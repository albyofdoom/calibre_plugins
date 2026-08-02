# Goal

The purpose of this Calibre plugin will be to collect the epub filenames from 2 selected files and open them in beyond compare. 

# Acceptance Criteria

1. A calibre action will be available as a keybinding and toolbar button
2. When either the keybinding or toolbar button are clicked and 2 or 3 books are selected and all selected books have ePub versions, it will launch beyond compare to compare the files.
3. If 1 book is selected it will open beyond compare but only pass the selected epub file to the left pane.
4. If 4 or more books are selected, no action will be taken, and no warnings will be given. 

## Beyond Compare Syntax Reference


BCompare.exe: This is the main application.  Only one copy will run at a time, regardless of how many windows you have open.  If you launch a second copy it will tell the existing copy to start a comparison and exit immediately.

### Command line parameters

Notice that each parameter should be enclosed in quotation marks if it might contain a space.

| Parameter                    | Meaning                                                                                                                                                                           |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Named Session                | Opens the specified session in the appropriate view.  For example: ` BCompare.exe "My Session"`                                                                                   |
| Named Workspace              | Opens the specified saved workspace.  (see also Managing Workspaces)  For example: ` BCompare.exe "My Special Workspace"`                                                         |
| Pair of folders              | Opens a new Folder Compare view with the specified base folders.  For example:  ` BCompare.exe "C:\Left Folder" "C:\Right Folder"`                                                |
| Pair of files                | Opens the specified files in the associated file view.  For example: ` BCompare.exe "C:\Left File.ext" "C:\Right File.ext"`                                                       |
| 3 files                      | Opens a Text Merge view with the specified files in the left, right, and center panes.  For example: ` BCompare.exe C:\Left.ext C:\Right.ext C:\Center.ext`                       |
| 4 files                      | Opens a Text Merge view with the specified files in the left, right, center, and output panes.  For example: ` BCompare.exe C:\Left.ext C:\Right.ext C:\Center.ext C:\Output.ext` |
| Script file                  | Automatically executes a list of commands without using a view.  For example: ` BCompare.exe "@C:\My Script.txt"`                                                                 |
| Settings package (.bcpkg)    | Imports settings from package.                                                                                                                                                    |
| Patch file (.diff or .patch) | Opens the specified file in the Text Patch view.                                                                                                                                  |
| -                            | Opens stdin in the appropriate view.  For example:  `dir \| BCompare.exe`                                                                                                           |