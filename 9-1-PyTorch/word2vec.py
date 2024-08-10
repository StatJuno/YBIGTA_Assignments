# word2vec.py

import torch
from torch import nn, Tensor, LongTensor
from torch.optim import Adam

from transformers import PreTrainedTokenizer

from typing import Literal, List


class Word2Vec(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        window_size: int,
        method: Literal["cbow", "skipgram"]
    ) -> None:
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, d_model)
        self.output_weights = nn.Linear(d_model, vocab_size, bias=False)
        self.window_size = window_size
        self.method = method

    def embeddings_weight(self) -> Tensor:
        return self.embeddings.weight.detach()

    def fit(
        self,
        corpus: List[str],
        tokenizer: PreTrainedTokenizer,
        lr: float,
        num_epochs: int
    ) -> None:
        criterion = nn.CrossEntropyLoss()
        optimizer = Adam(self.parameters(), lr=lr)

        # Tokenize the corpus
        tokenized_corpus = [tokenizer.encode(sentence, add_special_tokens=False) for sentence in corpus]

        # Training loop
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            for sentence in tokenized_corpus:
                # For each word in the sentence
                for i, target in enumerate(sentence):
                    # CBOW
                    if self.method == 'cbow':
                        start = max(0, i - self.window_size)
                        end = min(len(sentence), i + self.window_size + 1)
                        context = [sentence[j] for j in range(start, end) if j != i]
                        if len(context) == self.window_size * 2:
                            context_tensor = torch.tensor(context, dtype=torch.long).unsqueeze(0).to(next(self.parameters()).device)
                            target_tensor = torch.tensor([target], dtype=torch.long).to(next(self.parameters()).device)
                            loss = self._train_cbow(context_tensor, target_tensor, optimizer, criterion)
                            epoch_loss += loss.item()

                    # Skip-gram
                    elif self.method == 'skipgram':
                        for j in range(max(0, i - self.window_size), min(len(sentence), i + self.window_size + 1)):
                            if j != i:
                                context_tensor = torch.tensor([sentence[i]], dtype=torch.long).to(next(self.parameters()).device)
                                target_tensor = torch.tensor([sentence[j]], dtype=torch.long).to(next(self.parameters()).device)
                                loss = self._train_skipgram(context_tensor, target_tensor, optimizer, criterion)
                                epoch_loss += loss.item()

            print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {epoch_loss / len(tokenized_corpus):.6f}')

    def _train_cbow(
        self,
        context: Tensor,
        target: Tensor,
        optimizer: Adam,
        criterion: nn.CrossEntropyLoss
    ) -> Tensor:
        optimizer.zero_grad()
        embeddings = self.embeddings(context)  # [batch_size, window_size * 2, d_model]
        hidden = embeddings.mean(dim=1)  # [batch_size, d_model]
        output = self.output_weights(hidden)  # [batch_size, vocab_size]

        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        return loss

    def _train_skipgram(
        self,
        context: Tensor,
        target: Tensor,
        optimizer: Adam,
        criterion: nn.CrossEntropyLoss
    ) -> Tensor:
        optimizer.zero_grad()
        hidden = self.embeddings(context).squeeze(1)  # [batch_size, d_model]
        output = self.output_weights(hidden)  # [batch_size, vocab_size]

        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        return loss
