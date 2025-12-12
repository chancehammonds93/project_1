from PyQt6 import*
from gui import*

class Television:
    MIN_VOLUME = 0
    MAX_VOLUME = 4
    MIN_CHANNEL = 0
    MAX_CHANNEL = 3

    def __init__(self) -> None:
        """
        Method that creates a Television object.
        """
        self.__status = False
        self.__muted = False
        self.__volume = Television.MIN_VOLUME
        self.__channel = Television.MIN_CHANNEL

    def power(self) -> None:
        """
        Method that powers up the television object.
        """
        if not self.__status:
            self.__status = True
        elif self.__status:
            self.__status = False

    def mute(self) -> None:
        """
        Method that mutes the television object.
        """
        if self.__status:
            if not self.__muted:
                self.__muted = True
            elif self.__muted:
                self.__muted = False

    def channel_up(self) -> None:
        """
        Method that channels up the television object.
        """
        if self.__status:
            if self.__channel < Television.MAX_CHANNEL:
                self.__channel += 1
            elif self.__channel == Television.MAX_CHANNEL:
                self.__channel = Television.MIN_CHANNEL

    def channel_down(self) -> None:
        """
        Method that channels down the television object.
        """
        if self.__status:
            if self.__channel > Television.MIN_CHANNEL:
                self.__channel -= 1
            elif self.__channel == Television.MIN_CHANNEL:
                self.__channel = Television.MAX_CHANNEL

    def volume_up(self) -> None:
        """
        Method that increases volume of the television object by 1.
        """
        if self.__status:
            if self.__muted:
                self.__muted = False
            if self.__volume < Television.MAX_VOLUME:
                self.__volume += 1
            elif self.__volume == Television.MAX_VOLUME:
                pass

    def volume_down(self) -> None:
        """
        Method that decreases volume of the television object by 1.
        """
        if self.__status:
            if self.__muted:
                self.__muted = False
            if self.__volume > Television.MIN_VOLUME:
                self.__volume -= 1
            elif self.__volume == Television.MIN_VOLUME:
                pass

    def __str__(self) -> str:
        """
        Method to show the TV status.
        :return: TV status
        """
        return f'Power = {self.__status}, Channel = {self.__channel}, Volume = {self.__volume}'

    def is_on(self) -> bool: return self.__status
    def is_muted(self) -> bool: return self.__muted
    def get_volume(self) -> int: return self.__volume
    def get_channel(self) -> int: return self.__channel

channel_images = {
    0: "espn_logo.png",
    1: "cnn_logo.png",
    2: "cn_logo.png",
    3: "cbs_logo.png",
}

class Logic(QtWidgets.QMainWindow, Ui_GUI_Project):
    """
    Method that connects GUI to the Television object.
    """

    def __init__(self) -> None:
        """
        Initialize the GUI, and connect buttons/signals sets UI to initial state.
        """
        super().__init__()
        self.setupUi(self)

        self.tv = Television()
        self.volume_slider.setMinimum(Television.MIN_VOLUME)
        self.volume_slider.setMaximum(Television.MAX_VOLUME)
        self.volume_slider.setValue(self.tv.get_volume())
        self.remote_power_button.clicked.connect(self.power)
        self.channel_up_button.clicked.connect(self.channel_up)
        self.channel_down_button.clicked.connect(self.channel_down)
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_down_button.clicked.connect(self.volume_down)
        self.mute_button.clicked.connect(self.mute)
        self.volume_slider.valueChanged.connect(self.slider_changed)

        self.update_ui()

    def power(self) -> None:
        """
        Method that powers on/off the television object.
        """

        self.tv.power()
        self.update_ui()

    def channel_up(self) -> None:
        """
        Method that channels up the television object.
        """
        self.tv.channel_up()
        self.update_ui()

    def channel_down(self) -> None:
        """
        Method that channels down the television object.
        """
        self.tv.channel_down()
        self.update_ui()

    def volume_up(self) -> None:
        """
        Method that increases volume of the television object by 1.
        """
        self.tv.volume_up()
        self.volume_slider.setValue(self.tv.get_volume())
        self.update_ui()

    def volume_down(self) -> None:
        """
        Method that decreases volume of the television object by 1.
        """
        self.tv.volume_down()
        self.volume_slider.setValue(self.tv.get_volume())
        self.update_ui()

    def mute(self) -> None:
        """
        Method that mutes/unmutes the television object.
        """
        self.tv.mute()
        self.update_ui()

    def slider_changed(self,value) -> None:
        """
        Method that adjusts volume of television object.
        :param value: Value on the slider.
        """
        if not self.tv.is_on():
            self.volume_slider.setValue(self.tv.get_volume())
            return

        while self.tv.get_volume() < value:
            self.tv.volume_up()
        while self.tv.get_volume() > value:
            self.tv.volume_down()

        self.update_ui()

    def update_ui(self) -> None:
        """
        Method that updates the GUI. Disables buttons when power is off.
        """
        if not self.tv.is_on():
            self.channel_image.clear()
            self.channel_lcd.display(0)

            for widget in [
                self.channel_up_button,
                self.channel_down_button,
                self.volume_up_button,
                self.volume_down_button,
                self.mute_button,
                self.volume_slider,
            ]:
                widget.setEnabled(False)

            self.mute_label.setStyleSheet("color:white;")
            return

        for widget in [
            self.channel_up_button,
            self.channel_down_button,
            self.volume_up_button,
            self.volume_down_button,
            self.mute_button,
            self.volume_slider,
        ]:
            widget.setEnabled(True)

        chan = self.tv.get_channel()
        self.channel_lcd.display(chan)

        pix_path = channel_images.get(chan)
        if pix_path:
            pixmap = QtGui.QPixmap(pix_path)
            self.channel_image.setPixmap(pixmap)
            self.channel_image.setScaledContents(True)

        self.volume_slider.setValue(self.tv.get_volume())

        if self.tv.is_muted():
            self.mute_label.setStyleSheet("color:red;")
        else:
            self.mute_label.setStyleSheet("color:white;")