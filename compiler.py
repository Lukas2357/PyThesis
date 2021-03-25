import subprocess
import errno
import os


def generate_pdf(filepath, basename, *, compiler=None, compiler_args=None, silent=True):

    cwd = os.getcwd()
    os.chdir(filepath)

    if compiler_args is None:
        compiler_args = []

    if compiler is not None:
        compilers = ((compiler, []),)
    else:
        latexmk_args = ['--pdf']
        compilers = (('latexmk', latexmk_args), ('pdflatex', []))

    main_arguments = ['--interaction=nonstopmode', basename + '.tex']

    os_error = None

    for compiler, arguments in compilers:
        command = [compiler] + arguments + compiler_args + main_arguments

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)

        except (OSError, IOError) as e:
            # Use FileNotFoundError when python 2 is dropped
            os_error = e

            if os_error.errno == errno.ENOENT:
                # If compiler does not exist, try next in the list
                continue
            raise
        except subprocess.CalledProcessError as e:
            # For all other errors print the output and raise the error
            print(e.output.decode())
            raise
        else:
            if not silent:
                print(output.decode())

        # Compilation has finished, so no further compilers have to be
        # tried
        break

    else:
        # Notify user that none of the compilers worked.
        raise (TypeError(
            'No LaTex compiler was found\n' +
            'Either specify a LaTex compiler ' +
            'or make sure you have latexmk or pdfLaTex installed.'
        ))

    os.chdir(cwd)
