#  -----------------------------------------------------------  #
# | Application for convenient writing of book like documents | #
#  -----------------------------------------------------------  #

# ---------- Imports ---------------------------------------------------------------------------------------------------

import os
from os import path
import shutil
from pathlib import Path
from datetime import date, datetime
from compiler import generate_pdf
import tkinter as tk


# ---------- Functions -------------------------------------------------------------------------------------------------

def create_parameter(column, row, label, unit, default):
    label = tk.Label(text=label, anchor="e", width=16)
    label.grid(column=column, row=row)
    entry = tk.Entry(width=30)
    entry.grid(column=column + 1, row=row)
    entry.insert(tk.END, default)
    unit = tk.Label(text=unit, width=4)
    unit.grid(column=column + 2, row=row)
    return entry


def rmv_waste(file_path, file):
    waste = [f for f in os.listdir(file_path) if f.startswith(file) and not f.endswith('tex') and not f.endswith('pdf')]
    for waste_file in waste:
        os.remove(path.join(file_path, waste_file))


def copy_if_exist(source, file, destination, new_name=""):
    if path.exists(path.join(source, file)):
        shutil.copy(path.join(source, file), path.join(destination, new_name))


def copy_if_not_in_destination(source, file, destination):
    if not path.exists(path.join(destination, file)):
        shutil.copy(path.join(source, file), path.join(destination, file))


# ---------- Inputs ----------------------------------------------------------------------------------------------------

root = os.getcwd()
update_archive = True
compile_main = True
compile_overview = True
running = True

while running:

    if "initials.txt" not in os.listdir(root):
        param_window = tk.Tk()
        param_window.wm_title("Thesis Help")
        param_window.geometry('450x290')
        frame = tk.Frame(param_window)
        frame.grid()

        info_text = tk.Label(text='\nThis is a tool to help you writing your thesis in a convenient way. \n'
                                  'Please input first the path on your computer, where you want to place \n'
                                  'your project and the name of the projects folder. \n', width=62)
        info_text.grid(column=0, row=0, columnspan=2)
        path_input = create_parameter(0, 1, 'Folder Path:', '', "C:\\")
        folder_input = create_parameter(0, 2, 'Project Folder:', '', "THESIS")
        info_text = tk.Label(text='\nNow provide the kind of project you have and your name. \n'
                                  'Those information will be shown in an overview document of your project.\n',
                             width=62)
        info_text.grid(column=0, row=3, columnspan=2)
        typ_input = create_parameter(0, 4, 'Kind of Project:', '', "Master Thesis")
        author_input = create_parameter(0, 5, 'Author:', '', "Lukas Hunold")

        empty_text = tk.Label(text="")
        empty_text.grid(column=0, row=6, columnspan=2)


        def _proceed():
            param_window.quit()


        button = tk.Button(text="Proceed", command=_proceed)
        button.grid(column=0, row=7, columnspan=2)

        param_window.mainloop()

        folder = path_input.get()
        project = folder_input.get()
        typ = typ_input.get()
        author = author_input.get()

    else:
        param_window = tk.Tk()
        param_window.wm_title("Thesis Help")
        param_window.geometry('250x220')
        frame = tk.Frame(param_window)
        frame.grid()


        def getBool1():  # get rid of the event argument
            archive_boolvar.get()


        def getBool2():  # get rid of the event argument
            main_boolvar.get()


        def getBool3():  # get rid of the event argument
            overview_boolvar.get()

        def getBool4():  # get rid of the event argument
            bib_boolvar.get()


        info_text = tk.Label(text='\nOverview.tex will be updated. In addition:\n', width=35)
        info_text.grid(column=0, row=0)

        archive_boolvar = tk.BooleanVar()
        archive_boolvar.set(False)
        archive_boolvar.trace('w', lambda *_: print(""))
        archive = tk.Checkbutton(text="Update archive", variable=archive_boolvar, command=getBool1)
        archive.grid(column=0, row=1)

        overview_boolvar = tk.BooleanVar()
        overview_boolvar.set(False)
        overview_boolvar.trace('w', lambda *_: print(""))
        compile_overview = tk.Checkbutton(text="Compile overview", variable=overview_boolvar, command=getBool3)
        compile_overview.grid(column=0, row=2)

        main_boolvar = tk.BooleanVar()
        main_boolvar.set(False)
        main_boolvar.trace('w', lambda *_: print(""))
        compile_main = tk.Checkbutton(text="Compile main", variable=main_boolvar, command=getBool2)
        compile_main.grid(column=0, row=3)

        bib_boolvar = tk.BooleanVar()
        bib_boolvar.set(False)
        bib_boolvar.trace('w', lambda *_: print(""))
        update_bib = tk.Checkbutton(text="Update bib files", variable=bib_boolvar, command=getBool4)
        update_bib.grid(column=0, row=4)


        def _proceed():
            param_window.quit()

        def _proceed_and_quit():
            param_window.quit()
            global running
            running = False


        button = tk.Button(text="Proceed", command=_proceed)
        button.grid(column=0, row=7)

        button = tk.Button(text="Proceed and Quit", command=_proceed_and_quit)
        button.grid(column=0, row=8)

        param_window.mainloop()

        update_archive = archive_boolvar.get()
        compile_main = main_boolvar.get()
        compile_overview = overview_boolvar.get()
        update_bib = bib_boolvar.get()

        os.chdir(root)

        with open("initials.txt", "r+") as init_file:
            initials = init_file.read().splitlines()
            folder = initials[0]
            project = initials[1]
            typ = initials[2]
            author = initials[3]

    # ---------- Main --------------------------------------------------------------------------------------------------

    # Create project folder:
    project_path = path.join(folder, project)
    Path(project_path).mkdir(parents=True, exist_ok=True)
    # From now on stay in project folder:
    os.chdir(project_path)

    # Create sub-folders:
    for folder_name in ['MAIN', 'ORGA', 'ELSE', 'FILES']:
        Path(folder_name).mkdir(parents=True, exist_ok=True)
    for sub_folder_name in ['chapters', 'archive', 'configs']:
        Path(path.join("MAIN", sub_folder_name)).mkdir(parents=True, exist_ok=True)
    Path(path.join("ORGA", "archive")).mkdir(parents=True, exist_ok=True)

    # Copy LaTex class specification file and bib example file and Parts list example file:
    copy_if_not_in_destination(root, "thesisclass.cls", path.join("MAIN", "configs"))
    copy_if_not_in_destination(root, "Bib.bib", path.join("MAIN", "configs"))
    copy_if_not_in_destination(root, "0-0-Parts.txt", "ORGA")

    # Construct for each section .txt information files and input them to a .tex overview file.
    # Simultaneously create folders for each section, one with .tex files and one empty for other files:

    overview_file_title = "\\textbf{{\\underline{{Overview {} {} ~~~~ \\hspace{{90pt}} {}}}}} ". \
                              format(typ, author,
                                     date.today()) + "\n\\textcolor{white}{...} \\\\ \\textcolor{white}{...} \\\\"

    with open(path.join("ORGA", "0-0-Parts.txt"), 'r+') as parts_file:
        titles = parts_file.read().splitlines()
        titles_dict = {title.split("-")[0].strip(): titles[i].split("-")[1].split(",") for i, title in
                       enumerate(titles)}

    with open(path.join("ORGA", "0-0-Overview.tex"), "w+") as overview_file:
        with open(path.join(root, 'TexInput.txt'), 'r+') as overview_file_header:
            overview_file.write(overview_file_header.read() + overview_file_title)
        for chapter_number, chapter_title in enumerate(titles_dict.keys()):
            chapter_title = chapter_title.strip()
            chapter_filename = chapter_title.replace(" ", "-")
            chapter_fullname = "{}-{}".format(chapter_number, chapter_filename)
            chapter_texname = "{}.tex".format(chapter_filename)
            chapter_path = path.join("MAIN", "chapters", chapter_fullname)
            chapter_docs_path = path.join("FILES", chapter_fullname)
            overview_file.write("\n \n \n \\Part{{{}}}{{{}}}{{".format(chapter_number, chapter_title))
            Path(path.join(chapter_path)).mkdir(parents=True, exist_ok=True)
            if not os.path.exists(path.join(chapter_path, chapter_texname)):
                tex_input = "\\documentclass[../../main.tex]{{subfiles}}\n\n\\graphicspath{{{{pics/}}{{" \
                            "chapters/{}-{}/pics/}}}}\n\n\\begin{{document}}\n\\chapter{{{}}}\nContent...\n\\" \
                            "end{{document}}".format(chapter_number, chapter_filename, chapter_title)
                with open(path.join(chapter_path, chapter_texname), 'w+') as chapter_tex_file:
                    chapter_tex_file.write(tex_input)
                copy_if_exist(root, chapter_texname, chapter_path)
            Path(path.join(chapter_path, "configs")).mkdir(parents=True, exist_ok=True)
            if update_bib:
                copy_if_exist(path.join("MAIN", "configs"), "Bib.bib", path.join(chapter_path, "configs"))
            Path(path.join(chapter_path, "pics")).mkdir(parents=True, exist_ok=True)
            Path(chapter_docs_path).mkdir(parents=True, exist_ok=True)
            copy_if_exist(chapter_path, "{}.pdf".format(chapter_filename), chapter_docs_path)
            rmv_waste(chapter_path, chapter_filename)
            for section_number, section_title in enumerate(titles_dict[chapter_title]):
                section_title = section_title.strip()
                section_filename = section_title.replace(" ", "-")
                section_fullname = "{}-{}".format(section_number + 1, section_filename)
                section_texname = "{}.tex".format(section_filename)
                section_txt_filename = "{}-{}-{}.txt".format(chapter_number, section_number, section_title)
                section_txt_path = path.join("ORGA", section_txt_filename)
                section_path = path.join("MAIN", "chapters", chapter_fullname, section_fullname)
                section_docs_path = path.join("FILES", chapter_fullname, section_fullname)
                overview_file.write("\n \n    \\Section{{{}}}".format(section_title))
                Path(section_path).mkdir(parents=True, exist_ok=True)
                if not os.path.exists(path.join(section_path, section_texname)):
                    tex_input = "\\documentclass[../../../main.tex]{{subfiles}}\n\n\\graphicspath{{{{pics/}}{{chapters" \
                                "/{}-{}/{}-{}/pics/}}}}\n\n\\begin{{document}}\n\\section{{{}}}\nContent...\n\\end{{" \
                                "document}}".format(chapter_number, chapter_filename,
                                                    section_number + 1, section_filename, section_title)
                    with open(path.join(section_path, section_texname), 'w+') as section_tex_file:
                        section_tex_file.write(tex_input)
                    copy_if_exist(root, section_texname, section_path)
                Path(path.join(section_path, "configs")).mkdir(parents=True, exist_ok=True)
                if update_bib:
                    copy_if_exist(path.join("MAIN", "configs"), "Bib.bib", path.join(section_path, "configs"))
                Path(path.join(section_path, "pics")).mkdir(parents=True, exist_ok=True)
                Path(section_docs_path).mkdir(parents=True, exist_ok=True)
                copy_if_exist(section_path, "{}.pdf".format(section_filename), section_docs_path)
                rmv_waste(section_path, section_filename)

                if section_title == "Title Page":
                    copy_if_not_in_destination(root, "unilogo.png", path.join(section_path, "pics"))
                    copy_if_not_in_destination(root, "grouplogo.png", path.join(section_path, "pics"))

                if not path.exists(section_txt_path):
                    with open(section_txt_path, 'w+') as section_file:
                        section_file.write("Contents: \nDocuments: \nFolder: \nRemarks: ")

                with open(section_txt_path, 'r+') as section_file:
                    data = section_file.read().replace("Contents: ", '|').replace("\nDocuments: ", '|'). \
                        replace("\nFolder: ", '|').replace("\nRemarks: ", '|').split("|")
                    for entry in data[1:]:
                        overview_file.write("{{{}}}".format(entry))

                if (section_number + 1) % 3 == 0:
                    overview_file.write(" \n }} \n \n \\Part{{{}}}{{{}}}{{".format(chapter_number, chapter_title))

            overview_file.write("\n }")

        overview_file.write("\n \n \\end{document}")

    if compile_overview:
        generate_pdf("ORGA", "0-0-Overview", compiler="lualatex", compiler_args=None, silent=True)
        rmv_waste("ORGA", "0-0-Overview")

    with open(path.join("MAIN", "main.tex"), "w+") as main:
        with open(path.join(root, 'MainBegin.txt'), 'r+') as input_top:
            main.write(input_top.read())
        for chapter_number, chapter_title in enumerate(list(titles_dict.keys())[2:-2]):
            chapter_filename = chapter_title.strip().replace(" ", "-")
            main.write("\\Chapter{{{}}}{{{}}}\n".format(chapter_number + 2, chapter_filename))
            for section_number, section_title in enumerate(titles_dict[chapter_title]):
                section_filename = section_title.strip().replace(" ", "-")
                main.write("\\Section{{{}-{}}}{{{}}}{{{}}}\n".
                           format(chapter_number + 2, chapter_filename, section_number + 1, section_filename))
            main.write("\n")
        with open(path.join(root, 'MainEnd.txt'), 'r+') as input_bottom:
            main.write(input_bottom.read())

    if compile_main:
        generate_pdf("MAIN", "main", compiler="lualatex", compiler_args=None, silent=True)

    # And in the end copy existing stuff in archives:
    if update_archive:
        orga_archive_files = [file for file in os.listdir("ORGA") if path.isfile(path.join("ORGA", file))]
        for archive_file in orga_archive_files:
            shutil.copy(path.join("ORGA", archive_file), path.join("ORGA", "archive", archive_file))
        copy_if_exist("MAIN", "main.tex",
                      path.join("MAIN", "archive"), "main-{}.tex".format(datetime.now().strftime('%H-%M-%S-%m-%d')))
        shutil.copytree(path.join("MAIN", "chapters"),
                        path.join("MAIN", "archive", "chapters-{}".format(datetime.now().strftime('%H-%M-%S-%m-%d'))))
        if len(os.listdir(path.join("MAIN", "archive"))) > 25:
            print("\nYou have lots of stuff in the main archive. Consider deleting for memory safe!")

    if "initials.txt" not in os.listdir(root):
        param_window.destroy()

        info_window = tk.Tk()
        info_window.wm_title("Thesis Help")
        info_window.geometry('450x200')
        Frame = tk.Frame(info_window)
        Frame.grid()

        info_text = tk.Label(text="\nYou can now look into 0-0-Parts.txt file in your folder \\ORGA.\n"
                                  "Here you can insert your structure. Then run this program again.\n \n"
                                  "You get .txt files for each section, where you can write information, \n"
                                  "that will be place in the overview PDF file.\n \n"
                                  "0-0-Overview.pdf and main.pdf are generated each time you run this script.\n"
                                  "The .tex files of the sections can be compiled explicitely. \n", width=64)
        info_text.grid(column=0, row=1)


        def _quit():
            info_window.quit()


        button = tk.Button(text="Proceed", command=_quit)
        button.grid(column=0, row=2)

        info_window.mainloop()

        with open(path.join(root, "initials.txt"), "w+") as init_file:
            init_file.write(folder + "\n" + project + "\n" + typ + "\n" + author)
