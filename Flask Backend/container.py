class Container:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
    
    def __str__(self):
        return f"Container({self.id}, {self.weight})"
    
    def __repr__(self):
        return self.__str__()



def read_containers_from_file(filename: str):
    containers = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # .strip() is used to remove leading/trailing whitespace and split by the comma
                parts = line.strip().split(',')
                
                if len(parts) == 2:
                    name = parts[0].strip()  # Container name
                    weight = int(parts[1].strip())  # Convert weight to an integer (i think the values can have decimals?)
                    
                    
                    containers.append(Container(name, weight))  # take the input from the file and transform it into our defined container data type.
                else:
                    print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    
    return containers