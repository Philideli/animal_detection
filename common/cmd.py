from abc import ABC, abstractmethod


class CmdArgumentExtractor(ABC):

    def __init__(self, args=None):
        if not (args is None):
            self.args_dict = vars(self.get_parser().parse_args(args))
        else:
            self.args_dict = vars(self.get_parser().parse_args())

    @staticmethod
    @abstractmethod
    def get_parser():
        pass

    def get_extracted_arg(self, arg):
        return self.args_dict[arg] if (arg in self.args_dict) else None

    @abstractmethod
    def get_kwargs_for_execute(self):
        pass
