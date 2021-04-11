import torch
import torchvision.models as models
import torchvision.datasets as datasets
import torch.optim
import torch.utils.data
import argparse

CUDA = False

if __name__ == '__main__':

    # Paramètres en ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_path', default="", type=str, metavar='in_path', help='the path to the csv file contain the wav names and the GT')
    parser.add_argument('--in_channels', default=1, type=int, metavar='in_channels', help='the dimention of the input data')
    parser.add_argument('--out_channels', default=40, type=int, metavar="out_channels", help='the number of the classes')
    parser.add_argument('--epochs', default=1000, type=int, metavar='epochs', help='number of total epochs to run')
    parser.add_argument('--batch_size', default=32, type=int, metavar='batch_size', help='mini-batch size (default: 128)')
    parser.add_argument('--lr', default=0.1, type=float, metavar='lr', help='learning rate')
    parser.add_arguement('--validation_rate', default=0.2, type=float, metavar='validation_rate', help='the validation rate')
    parser.add_argument('--cuda', dest='cuda', action='store_true', help='activate GPU acceleration')

    args = parser.parse_args()
    if args.cuda:
        CUDA = True
        #cudnn.benchmark = True

    dataset = Audio(args.in_path, {"Good": 1, "Bad": 0}, is_num_classification=True)

    n_val = int(len(dataset) * args.validation_rate)
    n_train = len(dataset) - n_val

    trainset, valset = torch.utils.data.random_split(dataset,
                                                    [n_train, n_val])

    train_loader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers)

    val_loader = torch.utils.data.DataLoader(
        valset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers)


    model = models.resnet18(pretrained=True)
    model.conv1=nn.Conv2d(args.in_channels, model.conv1.out_channels,
                      kernel_size=model.conv1.kernel_size[0],
                      stride=model.conv1.stride[0],
                      padding=model.conv1.padding[0])
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(args.out_channels))

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    #train the model
    for i in range(args.epochs):
        print("=================\n=== EPOCH "+str(i+1)+" =====\n=================\n")
        for X, y in train_loader:
            X = X.double()
            y = y.long()
            if CUDA:
                X = X.cuda()
                y = y.cuda()

            model.zero_grad()
            output = model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            print(loss)

    #test the model
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in val_loader:
            X = X.double()
            y = y.long()
            if CUDA:
                X = X.cuda()
                y = y.cuda()
        output = model(X)
        for idx, i in enumerate(output):
            if torch.argmax(i) == y[idx]:
                correct += 1
            total += 1
    print("Accuracy: ", round(correct/total, 3))
