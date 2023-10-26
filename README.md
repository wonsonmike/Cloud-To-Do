# Overview

This is my first attempt with cloud storage. I want to learn the basics of how to store and manage data in the cloud. I will be using Google's Firebase to store the data. 

The software I've created is a basic to-do list. It stores the to-do items in the cloud as documents, and saves the name of the item and whether it's finished. If you finish an item, it will remove it from the list. The program is run by running the main.py file. It is used in a terminal, and will give you the options of viewing the list, adding an item, editing an item, and finishing an item. 

I wrote this software as a simple introduction to cloud databases. There are much better reasons to use a cloud database, but I wanted a very simple program as my first introduction with cloud storage. 

[Software Demo Video](https://youtu.be/JTTYUSwzqLw)

# Cloud Database

I am using Google's Firebase, and storing the data in their Firestore database. 

The database is very simply structured. There are two collections, one for the items on the to-do list and one for the log of changes. The items in the to-do list have the to-do item as the document name and whether it's done as a field in that document. 

# Development Environment

I used VSCode to program this software.

This program was made in Python, utilizing the firebase_admin library.

# Useful Websites

- [Documentation for Firestore database](https://firebase.google.com/docs/firestore)
- [Overview of Cloud Database basics](https://www.mongodb.com/cloud-database)

# Future Work

- Add the ability to create multiple to-do lists
- Let users decide to clear finished items or not
- Add better user interface