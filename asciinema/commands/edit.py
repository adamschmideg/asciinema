from asciinema.commands.command import Command
import asciinema.asciicast as asciicast
from asciinema.asciicast import v2


class EditCommand(Command):

    def __init__(self, source_files, target_file):
        self.source_files = source_files
        self.target_file = target_file

    def execute(self):
        try:
            header = None
            with asciicast.open_from_url(self.source_files[0]) as first_cast:
                header = first_cast.v2_header
            with v2.writer(self.target_file, header=header) as target:
                time_offset = 0
                for source in self.source_files:
                    with asciicast.open_from_url(source) as cast:
                        for ev in cast.events():
                            ts, etype, data = ev
                            ts += time_offset
                            target.write_event(ts, etype, data)
                    time_offset += v2.get_duration(source)

        except asciicast.LoadError as e:
            self.print_error("loading failed: %s" % str(e))
            return 1

        return 0