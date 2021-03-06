import subprocess


class IO(object):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if not "file_prefix" in kwargs:
                raise Exception("You must specify either two file names or file_prefix.")

            if "data_id" in kwargs:
                filename_prefix = "%s%d" % (kwargs["file_prefix"], kwargs["data_id"])
            else:
                filename_prefix = kwargs["file_prefix"]

            input_suffix = kwargs.get("input_suffix", ".in")
            output_suffix = kwargs.get("output_suffix", ".out")
            self.input_filename = filename_prefix + input_suffix
            self.output_filename = filename_prefix + output_suffix
        elif len(args) == 2:
            self.input_filename = args[0]
            self.output_filename = args[1]
        else:
            raise Exception("Invalid argument count")

        self.input_file = open(self.input_filename, 'w')
        self.output_file = open(self.output_filename, 'w')

    def __del__(self):
        try:
            self.input_file.close()
            self.output_file.close()
        except Exception:
            pass

    @staticmethod
    def __write(file, *args):
        for arg in args:
            file.write(str(arg))
            if arg != "\n":
                file.write(" ")

    def write(self, *args):
        IO.__write(self.input_file, *args)

    def writeln(self, *args):
        args = list(args)
        args.append("\n")
        self.write(*args)

    def output_gen(self, shell_cmd):
        self.input_file.close()
        with open(self.input_filename, 'r') as f:
            self.output_file.write(subprocess.check_output(shell_cmd, shell=True, stdin=f))

        self.input_file = open(self.input_filename, 'a')

    def output_write(self, *args):
        IO.__write(self.output_file, *args)

    def output_writeln(self, *args):
        args = list(args)
        args.append("\n")
        self.output_write(*args)
