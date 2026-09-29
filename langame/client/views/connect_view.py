"""Host / port / name form with a Connect button."""
from tkinter import ttk


class ConnectView(ttk.Frame):

    def __init__(self, parent, on_connect, default_host: str, default_port: int):
        super().__init__(parent, padding=20)
        self.on_connect = on_connect
        # TODO stage 5: three labelled Entries (host, port, name) + a button that
        # reads them and calls on_connect(host, int(port), name.strip()).
        # Bind <Return> to the same action.
        raise NotImplementedError
