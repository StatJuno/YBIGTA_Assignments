# gru.py
import torch
from torch import nn, Tensor


class GRUCell(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Weights for update gate z
        self.W_z = nn.Linear(input_size, hidden_size)
        self.U_z = nn.Linear(hidden_size, hidden_size)

        # Weights for reset gate r
        self.W_r = nn.Linear(input_size, hidden_size)
        self.U_r = nn.Linear(hidden_size, hidden_size)

        # Weights for candidate hidden state
        self.W_h = nn.Linear(input_size, hidden_size)
        self.U_h = nn.Linear(hidden_size, hidden_size)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        # Update gate
        z_t = torch.sigmoid(self.W_z(x) + self.U_z(h))
        # Reset gate
        r_t = torch.sigmoid(self.W_r(x) + self.U_r(h))
        # Candidate hidden state
        h_tilde = torch.tanh(self.W_h(x) + self.U_h(r_t * h))
        # New hidden state
        h_t = (1 - z_t) * h + z_t * h_tilde

        return h_t


class GRU(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.cell = GRUCell(input_size, hidden_size)

    def forward(self, inputs: Tensor) -> Tensor:
        batch_size, sequence_length, _ = inputs.size()
        h_t = torch.zeros(batch_size, self.hidden_size, device=inputs.device)

        # Iterate through the sequence
        for t in range(sequence_length):
            x_t = inputs[:, t, :]
            h_t = self.cell(x_t, h_t)

        # Return the last hidden state
        return h_t
