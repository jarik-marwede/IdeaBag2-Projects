#!/usr/bin/env python3
"""

Title:
Mp3 Player (and Other Formats)

Description:
A simple program for playing your favorite music files.
It should have the ability to Play, Pause, Fast Forward,
Rewind, Next, Previous, Repeat Once, Repeat Forever and Randomly Shuffle.
For extra complexity
see if you can add the ability to create playlists and an equalizer.
You could also generate a Like/Dislike playlist
by rating songs based on if a song is skipped or played to the end
or if the volume is increased/decreased whilst the song is being played.
"""
import os
import random
import tkinter as tk
from tkinter import filedialog, ttk

import pygame
from pygame import mixer as media_player

SONG_END_EVENT = pygame.USEREVENT + 1
DEFAULT_VOLUME = 0.5


class MainWindow(tk.Tk):
    """Tkinter root window."""

    def __init__(self):
        """Initialize window."""
        super().__init__()
        self.title("Mp3 Player")
        self.resizable(width=True, height=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # define variables
        self.repeat_forever = tk.BooleanVar(self,
                                            value=False)
        self.repeat = False
        self.currently_playing = tk.StringVar(self)
        self.current_index = None
        self.paused = False
        self.time_played = tk.StringVar(self)

        # create frames
        self.treeview_frame = ttk.Frame(self)
        self.volume_frame = ttk.Frame(self)
        self.currently_playing_frame = ttk.Frame(self)
        self.time_played_frame = ttk.Frame(self)
        self.bottom_audio_buttons_frame = ttk.Frame(self)

        # create other widgets
        self.playlist_treeview = ttk.Treeview(self.treeview_frame,
                                              columns=("filename",),
                                              selectmode="browse",
                                              show="tree")
        self.playlist_scroll_x = ttk.Scrollbar(self.treeview_frame,
                                               command=self.playlist_treeview.xview,
                                               orient=tk.HORIZONTAL)
        self.playlist_scroll_y = ttk.Scrollbar(self.treeview_frame,
                                               command=self.playlist_treeview.yview,)
        self.playlist_treeview["xscrollcommand"] = self.playlist_scroll_x.set
        self.playlist_treeview["yscrollcommand"] = self.playlist_scroll_y.set
        self.currently_playing_label = ttk.Label(self.currently_playing_frame,
                                                 text="Currently playing: ")
        self.current_file_label = ttk.Label(self.currently_playing_frame,
                                            text="",
                                            textvariable=self.currently_playing)
        self.time_played_text_label = ttk.Label(self.time_played_frame,
                                                text="Time played: ")
        self.time_played_label = ttk.Label(self.time_played_frame,
                                           text="",
                                           textvariable=self.time_played)
        self.volume_label = ttk.Label(self.volume_frame,
                                      text="Volume: ")
        self.volume_scale = ttk.Scale(self.volume_frame,
                                      orient=tk.VERTICAL,
                                      from_=1,
                                      to=0,
                                      value=DEFAULT_VOLUME,
                                      command=change_volume)
        self.play_button = ttk.Button(self.bottom_audio_buttons_frame,
                                      text="Play",
                                      command=self.play_audio)
        self.pause_resume_button = ttk.Button(self.bottom_audio_buttons_frame,
                                              text="Pause",
                                              command=self.pause_resume)
        self.next_button = ttk.Button(self.bottom_audio_buttons_frame,
                                      text="Next",
                                      command=self.play_next_file)
        self.previous_button = ttk.Button(self.bottom_audio_buttons_frame,
                                          text="Previous",
                                          command=self.play_previous_file)
        self.repeat_once_button = ttk.Button(self.bottom_audio_buttons_frame,
                                             text="Repeat once",
                                             command=self.repeat_once)
        self.repeat_forever_checkbutton = ttk.Checkbutton(self.bottom_audio_buttons_frame,
                                                          text="Repeat forever",
                                                          variable=self.repeat_forever)
        self.shuffle_playlist_button = ttk.Button(self.bottom_audio_buttons_frame,
                                                  text="Shuffle",
                                                  command=self.shuffle_playlist)
        self.main_menu = tk.Menu(self,
                                 tearoff=0)
        self.file_sub_menu = tk.Menu(self.main_menu,
                                     tearoff=0)

        # configure playlist_treeview
        self.playlist_treeview.column("#0",
                                      minwidth=0,
                                      width=0)
        self.playlist_treeview.column("filename",
                                      width=750)
        self.playlist_treeview.heading("filename",
                                       text="Filename",
                                       anchor=tk.CENTER)

        # configure main menu
        self.config(menu=self.main_menu)
        self.main_menu.add_cascade(menu=self.file_sub_menu,
                                   label="File")

        # configure file sub menu
        self.file_sub_menu.add_command(label="Open file(s)",
                                       command=self.open_file)
        self.file_sub_menu.add_command(label="Open playlist",
                                       command=self.open_playlist)
        self.file_sub_menu.add_separator()
        self.file_sub_menu.add_command(label="Exit",
                                       command=self.destroy)

        # display frames
        self.treeview_frame.grid(row=0, column=0, padx=40, pady=10, sticky=tk.NSEW)
        self.volume_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)
        self.currently_playing_frame.grid(row=1, column=0, padx=10, pady=10)
        self.time_played_frame.grid(row=2, column=0, padx=10, pady=10)
        self.bottom_audio_buttons_frame.grid(row=3, column=0, padx=40, pady=10)

        # display other widgets
        self.playlist_treeview.grid(row=0, column=0, sticky=tk.NSEW)
        self.playlist_scroll_y.grid(row=0, column=1, sticky=tk.NS)
        self.playlist_scroll_x.grid(row=1, column=0, sticky=tk.EW)
        self.volume_label.grid(row=0, column=0)
        self.volume_scale.grid(row=1, column=0, sticky=tk.NS)
        self.currently_playing_label.grid(row=0, column=0, padx=10)
        self.current_file_label.grid(row=1, column=0, padx=10, pady=5)
        self.time_played_text_label.grid(row=0, column=0)
        self.time_played_label.grid(row=1, column=0)
        self.shuffle_playlist_button.grid(row=0, column=0, padx=5)
        self.previous_button.grid(row=0, column=1, padx=5)
        self.play_button.grid(row=0, column=2, padx=5)
        self.pause_resume_button.grid(row=0, column=3, padx=5)
        self.next_button.grid(row=0, column=4, padx=5)
        self.repeat_once_button.grid(row=0, column=5, padx=5)
        self.repeat_forever_checkbutton.grid(row=0, column=6, padx=5)

        # configure grid
        self.treeview_frame.grid_columnconfigure(0, weight=1)
        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.volume_frame.grid_rowconfigure(1, weight=1)

        # create bindings
        self.playlist_treeview.bind("<Double-Button-1>",
                                    lambda _: self.play_audio())

        # load media player
        pygame.init()
        media_player.init()
        media_player.music.set_endevent(SONG_END_EVENT)

    def play_audio(self, file: tuple=None):
        """Play the currently selected file."""
        if not file:
            selection = self.playlist_treeview.selection()
            if selection:
                self.currently_playing.set(self.playlist_treeview.item(selection, "values")[0])
                self.current_index = self.playlist_treeview.index(selection)
                media_player.music.load(self.currently_playing.get())
                media_player.music.play()
                self.update_time_played()
        else:
            self.currently_playing.set(file[0])
            self.current_index = file[1]
            media_player.music.load(self.currently_playing.get())
            media_player.music.play()
            self.update_time_played()

    def pause_resume(self):
        """Pause the audio that is currently playing/resume playing it."""
        if self.paused:
            media_player.music.unpause()
            self.pause_resume_button.config(text="Pause")
            self.paused = False
        elif media_player.music.get_busy():
            media_player.music.pause()
            self.pause_resume_button.config(text="Resume")
            self.paused = True

    def play_next_file(self):
        """Play the next file in playlist."""
        if self.current_index:
            if self.repeat_forever.get():
                self.play_audio((self.currently_playing.get(),
                                 self.current_index))
            elif self.repeat:
                self.play_audio((self.currently_playing.get(),
                                 self.current_index))
                self.repeat = False
            else:
                new_index = self.current_index + 1
                if new_index >= len(self.playlist_treeview.get_children()):
                    return None
                new_item = self.playlist_treeview.get_children()[new_index]
                self.playlist_treeview.see(new_item)
                self.play_audio((self.playlist_treeview.item(new_item, "values")[0],
                                 new_index))

    def play_previous_file(self):
        """Play the previous file in playlist."""
        if self.current_index:
            new_index = self.current_index - 1
            if new_index < 0:
                return None
            new_item = self.playlist_treeview.get_children()[new_index]
            self.playlist_treeview.see(new_item)
            self.play_audio((self.playlist_treeview.item(new_item, "values")[0],
                             new_index))

    def repeat_once(self):
        """Repeat current file once."""
        self.repeat = True

    def shuffle_playlist(self):
        """Shuffle files in current playlist randomly."""
        old_entries = self.playlist_treeview.get_children()
        entries = [self.playlist_treeview.item(entry, "values") for entry in old_entries]
        random.shuffle(entries)
        self.playlist_treeview.delete(*old_entries)
        for entry in entries:
            self.playlist_treeview.insert("", "end", values=entry)

    def open_file(self):
        """Open new audio file."""
        files = filedialog.askopenfilenames(defaultextension=".mp3",
                                            filetypes=[("Mp3", "*.mp3")],
                                            parent=self)
        for file in files:
            self.playlist_treeview.insert("", "end", values=(file,))

    def open_playlist(self):
        """Open all audio files in a folder as a playlist."""
        directory = filedialog.askdirectory(parent=self)
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                file_path = directory + "/" + file
                self.playlist_treeview.insert("", "end", values=(file_path,))

    def event_checker(self):
        """Check whether the current audio file has ended."""
        for event in pygame.event.get():
            if event.type == SONG_END_EVENT:
                self.play_next_file()
        self.after(1, self.event_checker)

    def update_time_played(self):
        """Update the time the current file has been played."""
        time = round(media_player.music.get_pos() / 1000)
        self.time_played.set(str(time) + " seconds")
        self.after(500, self.update_time_played)


def change_volume(volume):
    """Change the volume to the specified volume."""
    media_player.music.set_volume(float(volume))


def _start_window():
    """Start the tkinter GUI."""
    main_window = MainWindow()
    main_window.after(1, main_window.event_checker)
    main_window.mainloop()


if __name__ == "__main__":
    _start_window()
