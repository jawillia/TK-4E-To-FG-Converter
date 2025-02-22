#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Name: DnD4eCharacterBuilderToFGConverterTool.py
Description: Provides the front-end desktop UI to convert Character Builder/CBLoader .dnd4e files 
                to xml files for Fantasy Grounds
Author: Jason Williams
Date: 2025-02-19
Version: 0.1
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path
from DnDXMLParser import readCBLoaderCharacterFile, readCBLoaderMainFile, writeFantasyGroundsFile
import xml.etree.ElementTree as ET

import json
import threading

import sv_ttk

def save_settings(mergedFileLocation, linksToPCOptionModule):
    settings = {"mergedFileLocation": mergedFileLocation, "linkTo4EPCOptionsModule": linksToPCOptionModule}
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        return {} #return an empty dictionary if the file is not found

def open_settings(root):
    def browseMergedFiles():
            mergedFile = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.xml*"),
                                                       ("all files",
                                                        "*.*")))
            mergedFileEntry.delete(0, 'end')
            mergedFileEntry.insert(0, mergedFile)

    settings_window = Toplevel()
    settings_window.transient(root)
    settings_window.title("Settings")

    x = root.winfo_x() + root.winfo_width()//2 - settings_window.winfo_reqwidth()//2
    y = root.winfo_y() + root.winfo_height()//2 - settings_window.winfo_reqheight()//2
    settings_window.geometry(f"+{root.winfo_x()}+{y}")

    saved_settings = load_settings()

    wrapperOptions = Frame(settings_window)
    wrapperOptions.pack(fill="both", expand="yes", padx=20, pady=15)

    mergedFileLabel = Label(wrapperOptions, text="Merged File Location:")
    mergedFileLabel.grid(row=0,column=0, padx=5, pady=10, sticky="W")
    mergedFile_var = StringVar(value=saved_settings.get("mergedFileLocation", "")) #Default value if not found
    mergedFileEntry = Entry(wrapperOptions, width=80, textvariable=mergedFile_var)
    mergedFileEntry.grid(row=0, column=1, columnspan=4, padx=5, pady=10)
    browseMergedFileButton = Button(wrapperOptions, text = 'Browse ...', width=10, command=browseMergedFiles)
    browseMergedFileButton.grid(row=0, column=5, padx=3, pady=10)

    linksToPCOptionModule_var = BooleanVar(value=saved_settings.get("linkTo4EPCOptionsModule", False))
    checkButton_linksToPCOptionModule = Checkbutton(wrapperOptions, text="Links to 4E PC Options Module (v2.0)", variable=linksToPCOptionModule_var)
    checkButton_linksToPCOptionModule.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    validationLabel = Label(wrapperOptions, padx=10, fg="red")

    def validateSave(mergedFile):
        tree = ET.parse(mergedFile)
        root = tree.getroot()
        if root.tag != "D20Rules":
            return "File is improperly formatted."

    def save_and_close():
        validationMessage = validateSave(mergedFileEntry.get())
        if validationMessage:
            validationLabel.config(text = validationMessage)
            validationLabel.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
        else:
            save_settings(mergedFile_var.get(), linksToPCOptionModule_var.get())
            settings_window.destroy()

    saveButton = Button(wrapperOptions, text="Save", command=save_and_close)
    saveButton.grid(row=3, column=5, columnspan=2, padx=5, pady=10, sticky="nsew")

def browseFiles(addButton, fileEntry):
    addButton.config(relief=SUNKEN) 
    filepath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.dnd4e*"),
                                                       ("all files",
                                                        "*.*")))
    if filepath:
        filename = os.path.basename(filepath)
        new_item = fileEntry.insert("", END, values=(filename, filepath))
        fileEntry.focus(new_item)
        fileEntry.selection_set(new_item)
    addButton.after(100, lambda: addButton.config(relief=RAISED))

def browseFolder(addFolderButton, fileEntry):
    addFolderButton.config(relief=SUNKEN) 
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_paths = [os.path.join(folder_path, file_path) for file_path in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_path))]
        for file_path in file_paths:
            _, file_extension = os.path.splitext(file_path)
            if file_extension == ".dnd4e":
                basefilename = os.path.basename(file_path)
                new_item = fileEntry.insert("", END, values=(basefilename, file_path))
                fileEntry.focus(new_item)
                fileEntry.selection_set(new_item)
      
    addFolderButton.after(100, lambda: addFolderButton.config(relief=RAISED)) 

def main():
    def browseOutputFiles():
        validationLabel.pack_forget()
        outputDirectory = filedialog.askdirectory()
        fileOutput.insert(0, outputDirectory)

    def open_file():
        validationLabel.pack_forget()
        if len(fileOutput.get()) > 0:
            os.system("start " + fileOutput.get())

    def remove_selected():
        selected_items = trv.selection()
        if len(selected_items) <= 0:
            validationLabel.config(text="Select at least one input file first.")
            validationLabel.pack(side=LEFT, padx=15)
        else:   
            validationLabel.pack_forget()
            for item in selected_items:
                trv.delete(item)

    def delete_tree_item_event(event):
        remove_selected()

    def flashButton(flashButton):
        flashButton.after(200, lambda: flashButton.configure(background="white"))
        flashButton.after(400, lambda: flashButton.configure(background="yellow"))
        flashButton.after(600, lambda: flashButton.configure(background="white"))

        flashButton.after(800, lambda: flashButton.configure(background="white"))
        flashButton.after(1000, lambda: flashButton.configure(background="yellow"))
        flashButton.after(1200, lambda: flashButton.configure(background="white"))


    def convert_all(progress_var, stop_flag, totalFiles, filesProcessed):
        while not stop_flag.is_set():
            trv_children = trv.get_children()
            children_count = len(trv_children)
            if children_count > 0 and len(fileOutput.get()) > 0:
                saved_settings = load_settings()
                mergedFile_var = saved_settings.get("mergedFileLocation", None)                
                root.update_idletasks()  # Update GUI
                totalFiles.set(children_count)
                progress_step = (100/children_count)/3
                for child_item in trv_children:
                    item_values = trv.item(child_item)['values']
                    if len(item_values) > 1:
                        data_file_path = item_values[1]
                        character = readCBLoaderCharacterFile(data_file_path)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI
                        character = readCBLoaderMainFile(character, mergedFile_var)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI
                        outputFilename = item_values[0]
                        outputFilename = Path(outputFilename).stem + ".xml"
                        output_data_file_path = os.path.join(fileOutput.get(), outputFilename)
                        writeFantasyGroundsFile(character, output_data_file_path)
                        filesProcessed.set(filesProcessed.get() + 1)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI
                        else:
                            stop_flag.set()
                progress_var.set(100)
                stop_flag.set()

    def convert_selected(progress_var, stop_flag, totalFiles, filesProcessed):
        while not stop_flag.is_set():
            selected_items = trv.selection()
            selected_item_count = len(selected_items)
            if selected_item_count > 0 and len(fileOutput.get()) > 0:
                saved_settings = load_settings()
                mergedFile_var = saved_settings.get("mergedFileLocation", None)
                root.update_idletasks()  # Update GUI
                totalFiles.set(selected_item_count)
                progress_step = (100/selected_item_count)/3
                for selected_item in selected_items:
                    item_values = trv.item(selected_item)['values']
                    if len(item_values) > 1:
                        data_file_path = item_values[1]
                        character = readCBLoaderCharacterFile(data_file_path)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI                        
                        character = readCBLoaderMainFile(character)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI                        
                        if len(fileOutput.get()) > 0:
                            outputFilename = item_values[0]
                            outputFilename = Path(outputFilename).stem + ".xml"
                            output_data_file_path = os.path.join(fileOutput.get(), outputFilename)
                        writeFantasyGroundsFile(character, output_data_file_path) 
                        filesProcessed.set(filesProcessed.get() + 1)
                        if progress_var.get() < 100:
                            progress_var.set(progress_var.get() + progress_step)
                            root.update_idletasks()  # Update GUI 
                        else:
                            stop_flag.set()
                progress_var.set(100)
                stop_flag.set()              

    def update_progress_bar(progress_var, pb, completeLabel, root, totalFiles, filesProcessed):
        pb['value'] = progress_var.get()
        if pb['value'] >= 100:
            completeLabel.config(text = "Download complete!", fg="green")
            completeLabel.pack(side=LEFT)
            if cancelConvertButtonBottom["state"] == NORMAL:
                cancelConvertButtonBottom["state"] = DISABLED
            flashButton(openOutputButtonBottom)
        elif pb['value'] < 100 and stop_flag.is_set():
            conversionMessage = f"Canceled ({filesProcessed.get()} out of {totalFiles.get()} files)"
            completeLabel.config(text = conversionMessage, fg="red")
            completeLabel.pack(side=LEFT) 
            if cancelConvertButtonBottom["state"] == NORMAL:
                cancelConvertButtonBottom["state"] = DISABLED
        else:
            conversionMessage = f"Converting {filesProcessed.get()} out of {totalFiles.get()} files..."
            completeLabel.config(text = conversionMessage, fg="black")
            completeLabel.pack(side=LEFT)
        if not stop_flag.is_set():
            root.after(100, update_progress_bar, progress_var, pb, completeLabel, root, totalFiles, filesProcessed) 

    def stop_progress():
        global stop_flag
        if stop_flag:
            stop_flag.set()

    def start_convertall_task():
        global stop_flag
        stop_flag = threading.Event()
        progress_var = IntVar();
        stop_event = threading.Event()
        thread = None
        totalFiles = IntVar();
        filesProcessed = IntVar();

        if len(fileOutput.get()) <= 0:
            validationLabel.config(text="Insert an output folder first.")
            validationLabel.pack(side=LEFT, padx=15)
        elif len(trv.get_children()) <= 0:
            validationLabel.config(text="Insert an input file first.")
            validationLabel.pack(side=LEFT, padx=15)
        else:
            validationLabel.pack_forget()
            pb.pack(side = LEFT)
            cancelConvertButtonBottom["state"] = NORMAL
            update_progress_bar(progress_var, pb, completeLabel, root, totalFiles, filesProcessed)
            thread = threading.Thread(target=convert_all, args=(progress_var, stop_flag, totalFiles, filesProcessed))
            thread.start()

    def start_convertselected_task():
        global stop_flag
        stop_flag = threading.Event()
        progress_var = IntVar();
        stop_event = threading.Event()
        thread = None
        totalFiles = IntVar();
        filesProcessed = IntVar();

        #Validation
        if len(fileOutput.get()) <= 0:
            validationLabel.config(text="Insert an output folder first.")
            validationLabel.pack(side=LEFT, padx=15)
        elif len(trv.selection()) <= 0:
            validationLabel.config(text="Select at least one input file first.")
            validationLabel.pack(side=LEFT, padx=15)            
        else:
            validationLabel.pack_forget()
            pb.pack(side = LEFT)
            cancelConvertButtonBottom["state"] = NORMAL

            update_progress_bar(progress_var, pb, completeLabel, root, totalFiles, filesProcessed)

            thread = threading.Thread(target=convert_selected, args=(progress_var, stop_flag, totalFiles, filesProcessed))
            thread.start()        

    # Create the main window
    root = Tk()

    # root window title and dimension
    root.title("DnD 4E CBLoader to Fantasy Grounds Converter")
    # Set geometry (widthxheight)
    root.geometry('700x560')

    sv_ttk.use_light_theme()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create a menu
    # menu = Menu(root)
    # root.config(menu = menu)
    # fileMenu = Menu(menu)
    # menu.add_cascade(label = 'File', menu = fileMenu)
    # fileMenu.add_command(label='Add File...')
    # fileMenu.add_command(label='Add Folder...')
    # fileMenu.add_separator()
    # fileMenu.add_command(label='Clear File List')
    # fileMenu.add_separator()
    # fileMenu.add_command(label='Convert Selected File(s)')
    # fileMenu.add_command(label='Convert All Files')
    # fileMenu.add_separator()
    # fileMenu.add_command(label='Exit', command=root.quit)
    # optionsMenu = Menu(menu)
    # menu.add_cascade(label = 'Options', menu = optionsMenu)
    # optionsMenu.add_command(label='Settings', command=lambda: open_settings(root))
    # helpmenu = Menu(menu)
    # menu.add_cascade(label='Help', menu=helpmenu)
    # helpmenu.add_command(label='About')

    #Create frame for top buttons
    buttonFrame = Frame(root, height=50, padx=6, pady=10)

    #Create an image button to add file
    addPhoto = PhotoImage(file = os.path.join(script_dir, "resources", "Awicons-Vista-Artistic-Add.48.png"))  
    addButton = Button(buttonFrame, text = 'Add File', image = addPhoto, compound = TOP, width="60", height="65")
    addButton.pack(side = LEFT, padx=6) 
    #Create an image button to add a folder
    addFolderPhoto = PhotoImage(file = os.path.join(script_dir, "resources", "icons8-add-folder-48.png"))
    addFolderButton = Button(buttonFrame, text = 'Add Folder', image = addFolderPhoto, compound = TOP, width="60", height="65")    
    addFolderButton.pack(side=LEFT, padx=6)
    #Create an image button to remove a record
    removePhoto = PhotoImage(file = os.path.join(script_dir, "resources", "icons8-remove-48.png"))
    removeButton = Button(buttonFrame, text = 'Remove', image = removePhoto, compound = TOP, width="60", height="65", command=remove_selected)
    removeButton.pack(side=LEFT, padx=6)    
    #Create an image button to convert file
    convertPhoto = PhotoImage(file = os.path.join(script_dir, "resources", "icons8-convert-48.png"))
    convertButton = Button(buttonFrame, text = 'Convert All', image = convertPhoto, compound = TOP, width="60", height="65", command=start_convertall_task)
    convertButton.pack(side = LEFT, padx=6)
    #Create an image button to open settings
    optionsPhoto = PhotoImage(file = os.path.join(script_dir, "resources", "icons8-settings-48.png"))
    optionsButton = Button(buttonFrame, text = 'Settings', image = optionsPhoto, compound = TOP, width="60", height="65", command=lambda: open_settings(root))
    optionsButton.pack(side = LEFT, padx=6)    
    
    # Create a wrapper widget
    wrapperFileList = Frame(root)
    wrapperInputFile = LabelFrame(root, text = "Input File")
    wrapperOutputFile = LabelFrame(root, text = "Output Folder")
    wrapperBottomConvert = Frame(root)
    # wrapperParsedText = LabelFrame(root, text = "Parsed Text")

    buttonFrame.pack(side=TOP, fill="x", expand="no", padx=20, pady=5)
    wrapperFileList.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapperOutputFile.pack(fill="both", expand="no", padx=20, pady=10, ipadx=5, ipady=5)
    wrapperBottomConvert.pack(fill="both", expand="no", padx=20, pady=10)
    # wrapperParsedText.pack(fill="both", expand="yes", padx=20, pady=10)

    #File List Wrapper
    trv = ttk.Treeview(wrapperFileList, columns=(1,2), show="headings")
    trv.column(1,anchor=CENTER, stretch=NO, width=200)
    trv.heading(1, text="File Name")
    trv.column(2,anchor=CENTER, stretch=YES)
    trv.heading(2, text="File Location")
    trv.pack(fill=BOTH, padx=10, pady=10)

    validationLabel = Label(wrapperFileList, text = "warning", fg="red")
    #validationLabel.pack(side=LEFT, padx=15)

    #File Output
    fileOutput = Entry(wrapperOutputFile, width=80)
    fileOutput.pack(side=LEFT, padx=10)
    browseButton = Button(wrapperOutputFile, text = 'Browse ...', width=10, command=browseOutputFiles)
    browseButton.pack(side = LEFT) 
    openOutputButtonBottom = Button(wrapperOutputFile, text = 'Open', width=10, command=open_file)
    openOutputButtonBottom.pack(side = RIGHT, padx=10)      

    # progressbar
    pb = ttk.Progressbar(
        wrapperBottomConvert,
        orient='horizontal',
        mode='determinate',
        length=280
    )
    completeLabel = Label(wrapperBottomConvert, text="Download complete!", padx=15)

    #Create an alternative image button to convert file
    convertPhotoSmall = PhotoImage(file = os.path.join(script_dir, "resources", "icons8-convert-16.png"))
    convertButtonBottom = Button(wrapperBottomConvert, text = 'Convert', image = convertPhotoSmall, command=start_convertselected_task, compound = RIGHT, height=30, width=60, padx=6)
    convertButtonBottom.pack(side = RIGHT)
    cancelConvertButtonBottom = Button(wrapperBottomConvert, text = 'Cancel', command=stop_progress, height=1, width=10, padx=5, state=DISABLED)
    cancelConvertButtonBottom.pack(side = RIGHT, padx=10)

    #Events and Action Bindings
    addButton.bind("<Button-1>", lambda event: browseFiles(addButton, trv))
    addFolderButton.bind("<Button-1>", lambda event:browseFolder(addFolderButton, trv))
    trv.bind("<Delete>", delete_tree_item_event)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()