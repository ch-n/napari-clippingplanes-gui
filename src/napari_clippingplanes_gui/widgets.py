"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel
from qtpy.QtCore import Qt, Signal
from superqt import QRangeSlider
from typing import Any, Tuple

Horizontal = Qt.Orientation.Horizontal


class ClippingSliderWidget(QWidget):
    """Labeled widget with a range slider and a checkbox, for clipping planes control.

    Class attributes:
        - state_emitter: signal emitter for state_change events
        - value_emitter: signal emitter for state_change events
    """
    state_emitter = Signal([str, bool])
    value_emitter = Signal([str, tuple])

    def __init__(self, name: str, state: bool = False, srange: Tuple[int, int] = (0, 100), value: Tuple[int, int] = (0, 100)):
        """Initialise instance.

        :param name: slider name, will be displayed in the widget and can be used for identification
        :type name: str
        :param state: checkbox state, default: False
        :type state: bool
        :param srange: slider range, (min, max), default: (0, 100)
        :type srange: Tuple[int, int]
        :param value: slider values, position of the lower and upper bounds, default: (0, 100)
        :type value: Tuple[int, int]
        """
        super().__init__()
        self.name = name
        self.state = state
        self.range = srange
        self.value = value
        self._init_ui()
        self.set_state(self.state)
        self.set_range(*self.range)
        self.set_value(self.value)

    def _init_ui(self):
        """Initialise UI elements.
        """
        self.active_check = QCheckBox()
        self.rangeslider = QRangeSlider(Horizontal)

        self.active_check.stateChanged.connect(self.state_changed)
        self.rangeslider.valueChanged.connect(self.value_changed)

        layout = QHBoxLayout()
        layout.addWidget(self.active_check)
        layout.addWidget(QLabel(self.name))
        layout.addWidget(self.rangeslider)
        self.setLayout(layout)

    def set_state(self, state: bool):
        """Set to new state.
        Sets the state attribute of the instance and underlying QCheckbox to state and calls the state_changed() method.

        :param state: new state (Ture / False)
        :type state: bool
        """
        self.active_check.setChecked(state)

    def get_state(self) -> bool:
        """Return the current state.
        Extracts the state from the underlying QCheckbox.

        :return: State of the widget (True / False)
        :rtype: bool
        """
        return self.active_check.isChecked()

    def set_value(self, value: Tuple[int, int]):
        """Set to new state.
        Sets the value attribute of the instance and underlying QRangeSlider to value and calls the value_changed()
        method.

        :param value: new value tuple (lower, upper)
        :type value: Tuple[int, int]
        """
        self.rangeslider.setValue(value)

    def get_value(self) -> Tuple[Any, ...]:
        """Return the current value.
        Extracts the current value from the underlying QRangeSlider.

        :return: current value of the widget (lower, upper)
        :rtype: Tuple[Any, ...]
        """
        return self.rangeslider.value()

    def set_range(self, lower: float, upper: float):
        """Set range of the underlying slider.

        :param lower: minimal possible value of the slider
        :type lower: float
        :param upper: maximal possible value of the slider
        :type upper: float
        """
        self.rangeslider.setRange(lower, upper)
        self.range = self.get_range()

    def get_range(self) -> Tuple[float, float]:
        """Return the current range.
        Extracts the current range from the underlying QRangeSlider.

        :return: current range of the widget (min, max)
        :rtype: Tuple[float, float]
        """
        return self.rangeslider.minimum(), self.rangeslider.maximum()

    def state_changed(self) -> Tuple[str, bool]:
        """Emit state_changed signal.

        :return: name and new state of the instance
        :rtype: Tuple[str, bool]
        """
        self.state = self.get_state()
        return self.state_emitter.emit(self.name, self.state)

    def value_changed(self):
        """Emit value_changed signal.

        :return: name and new value of the instance
        :rtype: Tuple[str, Tuple[int, int]]
        """
        self.value = self.get_value()
        return self.value_emitter.emit(self.name, self.value)
