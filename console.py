#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import json

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

    def do_create(self, arg):
        """Create a new instance of BaseModel"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
        else:
            new_instance = BaseModel()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args or args[0] not in BaseModel.__subclasses__():
            print("** class name missing **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            obj_dict = storage.all()
            if key in obj_dict:
                print(obj_dict[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args or args[0] not in BaseModel.__subclasses__():
            print("** class name missing **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            obj_dict = storage.all()
            if key in obj_dict:
                del obj_dict[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        obj_list = []
        obj_dict = storage.all()
        if args and args[0] not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
            return
        for key, value in obj_dict.items():
            if not args or args[0] == value.__class__.__name__:
                obj_list.append(str(value))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = shlex.split(arg)
        obj_dict = storage.all()
        if not args or args[0] not in BaseModel.__subclasses__():
            print("** class name missing **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in obj_dict:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                instance = obj_dict[key]
                attr_name = args[2]
                attr_value = args[3]
                setattr(instance, attr_name, type(getattr(instance, attr_name))(attr_value))
                instance.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
