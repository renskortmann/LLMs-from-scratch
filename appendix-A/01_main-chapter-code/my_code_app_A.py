import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F

class NeuralNetwork(torch.nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super().__init__()

        self.layers = torch.nn.Sequential(

            # first hidden layer
            torch.nn.Linear(num_inputs, 30),
            torch.nn.ReLU(),

            # second hidden layer
            torch.nn.Linear(30, 20),
            torch.nn.ReLU(),

            # output layer
            torch.nn.Linear(20, num_outputs),
        )
    
    def forward(self, x):
        logits = self.layers(x)
        return logits

class ToyDataset(Dataset):
    def __init__(self, X, y):
        self.features = X
        self.labels = y

    def __getitem__(self, index):
        one_x = self.features[index]
        one_y = self.labels[index]
        return one_x, one_y
    
    def __len__(self):
        return self.labels.shape[0]

torch.manual_seed(123)
model = NeuralNetwork(50,3)

# print(model)

# num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
# print(f"Total number of parameters = {num_params}")

# print(model.layers[0].weight.shape)

# torch.manual_seed(123)
# X = torch.rand((1,50))
# with torch.no_grad():
#     out = torch.softmax(model(X), dim=-1)
# print(out)

X_train = torch.tensor([
    [-1.2, 3.1],
    [-0.9, 2.9],
    [-0.5, 2.6],
    [2.3, -1.1],
    [2.7, -1.5]    
])

y_train = torch.tensor([0, 0, 0, 1, 1])

X_test = torch.tensor([
    [-0.8, 2.8],
    [2.6, -1.6]
])

y_test = torch.tensor([0, 1])

train_ds = ToyDataset(X_train, y_train)
test_ds = ToyDataset(X_test, y_test)

# print(len(train_ds))

torch.manual_seed(123)
train_loader = DataLoader(
    dataset = train_ds,
    batch_size=2,
    shuffle=True,
    num_workers=0,
    drop_last=True
)

test_loader = DataLoader(
    dataset=test_ds,
    batch_size=2,
    shuffle=False,
    num_workers=0
)

# for idx, (x, y) in enumerate(train_loader):
#     print(f"Batch {idx+1}: ", x, y)

torch.manual_seed(123)
model = NeuralNetwork(num_inputs=2, num_outputs=2)
optimiser = torch.optim.SGD(model.parameters(), lr=0.5)

num_epochs = 3

for epoch in range(num_epochs):

    model.train()
    for batch_idx, (features, labels) in enumerate(train_loader):

        logits = model(features)

        loss = F.cross_entropy(logits, labels)

        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        print(f"Epoch: {epoch+1:03d}/{num_epochs:03d}"
              f" | Batch {batch_idx+1:03d}/{len(train_loader):03d}"
              f" | Train/Val Loss: {loss:.2f}"
        )

# model.eval()
# with torch.no_grad():
#     outputs = model(X_train)

# print(outputs)

# torch.set_printoptions(sci_mode=False)
# probas = torch.softmax(outputs, dim=-1)
# print(probas)

# predictions = torch.argmax(probas, dim=-1)
# print(predictions)
# print(predictions==y_train)

def compute_accuracy(model, dataloader):
    model.eval()
    correct = 0.0
    total_examples = 0

    for idx, (features, labels) in enumerate(dataloader):
        with torch.no_grad():
            logits = model(features)

        predictions = torch.argmax(torch.softmax(logits, dim=-1), dim=-1)
        compare = labels == predictions
        correct += torch.sum(compare)
        total_examples += len(compare)

    return (correct/total_examples).item()

print(f"correctness train_ds: {100*compute_accuracy(model, train_loader):.0f}%")
print(f"correctness test_ds: {100*compute_accuracy(model, test_loader):.0f}%")

# torch.save(model.state_dict(), "model.pth")

# model = NeuralNetwork(3,2)
# print(model.layers[0].weight)
# model = NeuralNetwork(2,2)
# print(model.layers[0].weight)

# model.load_state_dict(torch.load("model.pth", weights_only=True))
# print(model)
# print(model.layers[0].weight)