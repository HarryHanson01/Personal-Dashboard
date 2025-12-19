from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import QTimer
import psutil

class SystemStatsPanel(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("System Stats Panel")
        layout.addWidget(label)
        self.setLayout(layout)

        #self.setFixedSize(200, 300)

        # RAM and CPU
        self.cpuLabel = QLabel("CPU: ")
        layout.addWidget(self.cpuLabel)

        self.ramLabel = QLabel("RAM: ")
        layout.addWidget(self.ramLabel)

        # Disk and Network
        self.diskLabel = QLabel("Disk: ")
        layout.addWidget(self.diskLabel)

        self.networkLabel = QLabel("Network usage:")
        self.uploadLabel = QLabel("Upload: 0.0 Mbps")
        self.downloadLabel = QLabel("Download: 0.0 Mbps")
        layout.addWidget(self.networkLabel)
        layout.addWidget(self.uploadLabel)
        layout.addWidget(self.downloadLabel)
        
        self.lastNetIo = psutil.net_io_counters()

        # Timer to update stats 
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateStats)
        self.updateTimer.start(1000)  # currently updates every second


    def updateStats(self):
        cpuPercent = psutil.cpu_percent()
        self.cpuLabel.setText(f"CPU: {cpuPercent}%")
        
        ramPercent = psutil.virtual_memory().percent
        self.ramLabel.setText(f"RAM: {ramPercent}%")

        diskUsage = psutil.disk_usage("/").percent
        self.diskLabel.setText(f"Disk: {diskUsage}% used")


        uploadSpeed, downloadSpeed = self.calculateNetworkUsage()
        self.uploadLabel.setText(f"Upload: {uploadSpeed:.1f} Mbps")
        self.downloadLabel.setText(f"Download: {downloadSpeed:.1f} Mbps")



    def calculateNetworkUsage(self):
        new = psutil.net_io_counters()

        bytesSentPerSec = new.bytes_sent - self.lastNetIo.bytes_sent
        bytesRecvPerSec = new.bytes_recv - self.lastNetIo.bytes_recv

        self.lastNetIo = new

        # Convert Bps to Mbps
        upload = bytesSentPerSec * 8 / 1_000_000
        download = bytesRecvPerSec * 8 / 1_000_000

        return upload, download