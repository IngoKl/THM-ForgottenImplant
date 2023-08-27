# Creating Your Own VM

While *Forgotten Implant* has been designed as a [TryHackMe room](tryhackme.com/jr/forgottenimplant), you can build your own VM to play with. In the following you will find some key information on how to replicate the box yourself.

This is not meant as a comprehensive and detailed description or tutorial. Familiarity with Linux administration will be needed to follow along.

## Credentials

The VM has three accounts that need to be set up.

* SSH: fi:REDACTED
* SSH: ada:REDACTED
* MySQL: app:REDACTED

## 1. Setup and Configuration

Following TryHackMe's recommendation, start with clean installation of `Ubuntu 20.04` (server).

### Basics

The [Python code](room/code) and [server configuration](/room/config) can be found in this repository.

In order to get up and running, a few things need to be installed:

```bash
sudo apt install supervisor
sudo apt install python3-scapy
sudo apt install php php-cli php-mysqli php-xml php-curl composer
sudo apt install apache2 libapache2-mod-php
sudo apt install mysql-server

pip install mysql-connector-python
```

### Sniffer

The sniffer (`sniffer.py`) resides in `/home/fi`.

Place [sniffer.conf](room/config/sniffer.conf) in `/etc/supervisor/conf.d/` and run:

```bash
sudo supervisorctl update all
sudo supervisorctl restart sniffer
```

### Implant

The implant (`implant.py`) resides in `/home/ada/.implant`.

Set up a crontab for `ada`:
`* * * * * python3 /home/ada/.implant/implant.py`

### Vulnerable phpMyAdmin (4.8.1)

#### MySQL

Start a `MySQL` shell: `sudo mysql -u root`

```sql
CREATE DATABASE app;
CREATE USER 'app'@'localhost' IDENTIFIED WITH mysql_native_password BY 's4Ucbrme';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES ON app.* TO 'app'@'localhost';
CREATE TABLE `app`.`products` ( `id` INT NOT NULL AUTO_INCREMENT , `product` TEXT NOT NULL , `stock` INT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;

INSERT INTO `products` (`id`, `product`, `stock`) VALUES (NULL, 'Black Shirt, '4');
INSERT INTO `products` (`id`, `product`, `stock`) VALUES (NULL, 'Grey Scarf', '12');
INSERT INTO `products` (`id`, `product`, `stock`) VALUES (NULL, 'Pink Hat', '2');
```

#### Stored Credentials

The `products.py` file resides in `/home/ada/`. This script queries the database and contains the stored credentials.

#### Apache2

Place [000-default.conf](room/config/000-default.conf) in `/etc/apache2/sites-available/000-default.conf`.

In `/etc/apache2/ports.conf`, change the `Listen` setting to: `Listen 127.0.0.1:80`.

#### phpMyAdmin

The vulnerable version of `phpMyAdmin` resides in `/var/www/phpmyadmin`. In order to install `phpMyAdmin`, run:

```bash
wget https://github.com/phpmyadmin/phpmyadmin/archive/RELEASE_4_8_1.tar.gz

tar xfv RELEASE_4_8_1.tar.gz
mv phpmyadmin-RELEASE_4_8_1/ phpmyadmin
cd phpmyadmin
composer update --no-dev
cp config.sample.inc.php config.inc.php

mkdir /var/www/phpmyadmin/tmp
chmod 777 /var/www/phpmyadmin/tmp
```

Now, in `config.inc.php` set the `blowfish_secret`, e.g.:

`$cfg['blowfish_secret'] = 'umCmtcqJ8ah3j8SsY2GkJ4fbP8CryHX9';`

#### Sudo

Add `www-data     ALL=NOPASSWD: /usr/bin/php` to `/etc/sudoers`.

### Configure Ubuntu

```bash
sudo systemctl stop unattended-upgrades
sudo apt purge unattended-upgrades
sudo snap remove lxd
sudo snap remove core20
sudo snap remove snapd
sudo apt purge snap
```

## 3. Flag Placement

Place the following two flags:

* (local) ada: THM{REDACTED} in `/home/ada/user.txt`
* (system) root: THM{REDACTED} in `/root/.root.txt`

## 4. Sanitization

Before submitting or hosting the VM, it is advisable to remove as many of your traces as possible. While you certainly can da a lot more, the following is advised:

As `fi`:

```bash
unset HISTFILE
ln -s /dev/null /home/fi/.bash_history
ln -s /dev/null /home/fi/.python_history
```

As `ada`:

```bash
unset HISTFILE
ln -s /dev/null /home/ada/.bash_history
ln -s /dev/null /home/fi/.python_history
```

As `root`:

```bash
unset HISTFILE
ln -s /dev/null /root/.bash_history
ln -s /dev/null /root/.python_history
```

Furthermore, with `root` privileges, run [`sanitize.sh`](room/sanitize.sh).

Finally, disable `SSH` by running `sudo service ssh stop`.

## 5. Exporting to .ova

If you are using `VMWare Workstation`, in the "File > Export to OVF" dialogue, rename the export file to `Forgotten-Implant.ova`.

## 6. Additional Notes

### Notes on the Sniffer

Be aware that the sniffer, by default, only picks up on `10.X.X.X` IPs in order to limit everything to the THM network, for example not picking up on AWS traffic. This might hinder local testing.

On TryHackMe (hosted on AWS), the `/home/ada/.implant/hosts` file will contain a secondary IP. This IP belongs to an AWS monitoring service that will trigger the sniffer/implant.

### Notes on the C2 Implant and the C2 Controller

Both the [C2 Implant](room/code/implant.py) and the [C2 Controller](solution/c2.py) presented in the [walktrough](solution/official-walkthrough.md) have been specifically crafted for this challenge and are *not* meant as an example for how to build C2 software. They are both deeply flawed from a real-world perspective and have been designed as educational tools.

If you are interested in that, I can recommend, for example, Zero-Point Security's fantastic [*C2 Development in C#*](https://training.zeropointsecurity.co.uk/courses/c2-development-in-csharp) course.
