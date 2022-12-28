from data_loader import DataLoader

if __name__ == "__main__":
    data_loader = DataLoader("janos-us-ca.xml")
    print(data_loader.get_nodes()[0])
    print(data_loader.get_links()[0])
    print(data_loader.get_demands()[0])
