import torch
import torch.nn as nn

class ActivityCNN(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        # Assuming input spectrogram is 64x64
        self.fc = nn.Sequential(
            nn.Linear(32 * 16 * 16, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

class HeartLSTM(nn.Module):
    def __init__(self, input_size=52, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

class CsiAE(nn.Module):
    def __init__(self, input_size=52):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_size)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

if __name__ == "__main__":
    print("Mock training script.")
    # In a real scenario, we would load the .h5 dataset here and train the models.
    # For now, we instantiate and save them.
    import os
    os.makedirs("models", exist_ok=True)
    
    cnn = ActivityCNN()
    torch.save(cnn.state_dict(), "models/activity_cnn.pt")
    
    lstm = HeartLSTM()
    torch.save(lstm.state_dict(), "models/heart_lstm.pt")
    
    ae = CsiAE()
    torch.save(ae.state_dict(), "models/csi_ae.pt")
    
    print("Models saved to models/")
