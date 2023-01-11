import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox, QPushButton
import json

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the "Particles" field with a checkbox for turning it on/off
        self.particles_label = QLabel("Particles")
        self.particles_checkbox = QCheckBox()
        self.particles_checkbox.stateChanged.connect(self.handleParticlesChanged)
        self.particles_layout = QHBoxLayout()
        self.particles_layout.addWidget(self.particles_label)
        self.particles_layout.addWidget(self.particles_checkbox)

        # Create the "Car Icons" field with a checkbox for turning it on/off
        self.car_icons_label = QLabel("Car Icons")
        self.car_icons_checkbox = QCheckBox()
        self.car_icons_checkbox.stateChanged.connect(self.handleCarIconsChanged)
        self.car_icons_layout = QHBoxLayout()
        self.car_icons_layout.addWidget(self.car_icons_label)
        self.car_icons_layout.addWidget(self.car_icons_checkbox)

        # Create the "Speedometer" field with a checkbox for turning it on/off
        self.speedometer_label = QLabel("Speedometer")
        self.speedometer_checkbox = QCheckBox()
        self.speedometer_checkbox.stateChanged.connect(self.handleSpeedometerChanged)
        self.speedometer_layout = QHBoxLayout()
        self.speedometer_layout.addWidget(self.speedometer_label)
        self.speedometer_layout.addWidget(self.speedometer_checkbox)
        
        # Create a box where you place a number with a label "laps"
        self.laps_label = QLabel("Laps")
        self.laps_spinbox = QSpinBox()
        self.laps_layout = QHBoxLayout()
        self.laps_layout.addWidget(self.laps_label)
        self.laps_layout.addWidget(self.laps_spinbox)

        # Create one where it says "fps" and you also put a number
        self.fps_label = QLabel("FPS")
        self.fps_spinbox = QSpinBox()
        self.fps_layout = QHBoxLayout()
        self.fps_layout.addWidget(self.fps_label)
        self.fps_layout.addWidget(self.fps_spinbox)
        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.particles_layout)
        self.main_layout.addLayout(self.car_icons_layout)
        self.main_layout.addLayout(self.speedometer_layout)
        self.main_layout.addLayout(self.laps_layout)
        self.main_layout.addLayout(self.fps_layout)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.save_settings)
        self.main_layout.addWidget(self.apply_button)
        self.setLayout(self.main_layout)

    def handleParticlesChanged(self, state):
        if state == Qt.Checked:
            print("Particles turned on")
        else:
            print("Particles turned off")
            
    def handleCarIconsChanged(self, state):
        if state == Qt.Checked:
            print("Car Icons turned on")
        else:
            print("Car Icons turned off")
            
    def handleSpeedometerChanged(self, state):
        if state == Qt.Checked:
            print("Speedometer turned on")
        else:
            print("Speedometer turned off")

    def save_settings(self):
        settings = {
            "particles": str(self.particles_checkbox.isChecked()),
            "car_icon": str(self.car_icons_checkbox.isChecked()),
            "speedometer": str(self.speedometer_checkbox.isChecked()),
            "laps": self.laps_spinbox.value(),
            "fps": self.fps_spinbox.value()
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    widget.save_settings()
    sys.exit(app.exec_())
