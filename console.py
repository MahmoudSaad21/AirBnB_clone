#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""

import cmd

class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""
    
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        exit()

    def do_EOF(self, arg):
        """Exit the program on EOF"""
        print('')
        exit()

    def emptyline(self):
        """Do nothing on an empty line"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
