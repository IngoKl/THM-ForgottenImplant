# TryHackMe Room – Forgotten Implant

![Banner](room_design/banner.png)

Welcome to **Forgotten Implant**, a *TryHackMe* challenge in which, with almost no attack surface, you will have to use a forgotten C2 implant on the machine in order to get initial access.

> With limited attack surface comes limited possibilities. – TryHackMe

The room has been released on [*TryHackMe* as *Forgotten Implant*](https://tryhackme.com/room/forgottenimplant) on July 28th, 2023.

## 1. Learning Objectives and Prerequisites

This room is meant as a learning experience for intermediate and experienced hackers – beginners can absolutely do it, but it will be stretch! On TryHackMe, the room is ranked as *medium*. Based on reviewer feedback, it is on the top end of *medium*.

If learners have no experience with Command and Control (C2), TryHackMe's [Intro to C2](https://tryhackme.com/room/introtoc2) is a recommended prerequisite.

Hacking your way through this room, you will learn how to ...

* use tools like `Wireshark` to monitor network traffic.
* use `HTTP`, `Base64`, and `JSON` in the context of a simple HTTP client-server architecture.
* reverse engineer a simple C2 protocol.
* build a simple C2 interface using `Python` in order to interface with a C2 implant.
* leverage stored credentials in order to move laterally.
* exploit `phpMyAdmin` (4.8.1) using a public RCE exploit.
* leverage `sudo` and `PHP` in order to escalate privileges.

If you are interested in the Learning Experience Design (LXD), consider looking at the [accompanying article](https://kleiber.me/blog/2023/08/27/forgotten-implant-on-tryhackme-learning-experience-design/) discussing some of the LXD considerations.

## 2. Walkthrough

A [creator walkthrough](solution/official-walkthrough.md) is available that demonstrates and discusses how the room can be solved.

There are also several [community writeups and walkthroughs](https://github.com/IngoKl/THM-ForgottenImplant/blob/main/solution/writeups-and-walkthroughs.md) available. Some of these cover highly interesting (alternative) approaches.

Before looking at this (or any other) walkthrough or the hints towards [building your own machine](CREATE_VM.md), try to go through the machine on your own!

### TryHackMe Note

As this is an active challenge machine on TryHackMe, some of the files in this repository contain *REDACTED* information. 

While the information in this repository clearly is enough to solve the challenge, the redacted information (e.g., flags or credentials) could be used to simply grab the points/challenge without even attempting to do it. Hence, they have been removed.

## 3. Creating Your Own VM

If you are interested in building your own VM, have a look at [CREATE_VM.md](CREATE_VM.md).
