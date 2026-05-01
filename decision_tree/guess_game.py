import json
import os


class DecisionTreeNode:
    """Represents a node in the decision tree."""
    
    def __init__(self, question=None, yes_branch=None, no_branch=None, animal=None):
        self.question = question  # Question to ask at this node
        self.yes_branch = yes_branch  # Node if answer is yes
        self.no_branch = no_branch  # Node if answer is no
        self.animal = animal  # Animal name if this is a leaf node


class AnimalGuessingGame:
    """An interactive animal guessing game using decision trees."""
    
    def __init__(self, tree_file='animal_tree.json'):
        self.tree_file = tree_file
        self.root = None
        self.load_or_create_tree()
    
    def load_or_create_tree(self):
        """Load tree from file or create a default one."""
        if os.path.exists(self.tree_file):
            self.root = self.load_tree_from_file()
            print(f"✓ Tree loaded from {self.tree_file}")
        else:
            self.root = self.create_default_tree()
            self.save_tree_to_file()
            print("✓ Default tree created and saved")
    
    def create_default_tree(self):
        """Create a default decision tree with animals."""
        # Build tree from bottom up (leaf nodes first)
        
        # MAMMALS - Land - Wild - Fur
        lion = DecisionTreeNode(animal="Lion")
        tiger = DecisionTreeNode(animal="Tiger")
        bear = DecisionTreeNode(animal="Bear")
        wolf = DecisionTreeNode(animal="Wolf")
        
        # MAMMALS - Land - Wild - No Fur (scales/skin)
        crocodile = DecisionTreeNode(animal="Crocodile")
        python = DecisionTreeNode(animal="Python")
        
        # MAMMALS - Land - Domestic - Fur
        dog = DecisionTreeNode(animal="Dog")
        cat = DecisionTreeNode(animal="Cat")
        cow = DecisionTreeNode(animal="Cow")
        horse = DecisionTreeNode(animal="Horse")
        
        # MAMMALS - Water - Wild - Fur
        dolphin = DecisionTreeNode(animal="Dolphin")
        whale = DecisionTreeNode(animal="Whale")
        
        # MAMMALS - Water - Domestic - Fur
        beaver = DecisionTreeNode(animal="Beaver")
        
        # NON-MAMMALS - Water - Wild - No Fur
        shark = DecisionTreeNode(animal="Shark")
        octopus = DecisionTreeNode(animal="Octopus")
        
        # NON-MAMMALS - Land - Wild - No Fur
        penguin = DecisionTreeNode(animal="Penguin")
        ostrich = DecisionTreeNode(animal="Ostrich")
        
        # NON-MAMMALS - Air - Wild - No Fur
        eagle = DecisionTreeNode(animal="Eagle")
        parrot = DecisionTreeNode(animal="Parrot")
        
        # Build tree structure
        
        # Land mammals - Wild - with fur - big vs small
        land_wild_fur_big = DecisionTreeNode(
            question="Is it a big cat (lion/tiger) or bear-like?",
            yes_branch=lion,
            no_branch=tiger
        )
        
        land_wild_fur_small = DecisionTreeNode(
            question="Does it hunt in packs?",
            yes_branch=wolf,
            no_branch=bear
        )
        
        land_wild_fur = DecisionTreeNode(
            question="Is it one of the biggest land mammals?",
            yes_branch=land_wild_fur_big,
            no_branch=land_wild_fur_small
        )
        
        # Land mammals - Wild - no fur (reptiles)
        land_wild_no_fur = DecisionTreeNode(
            question="Does it live in water too (semi-aquatic)?",
            yes_branch=crocodile,
            no_branch=python
        )
        
        # Land mammals - Wild - combined
        land_wild = DecisionTreeNode(
            question="Does it have fur?",
            yes_branch=land_wild_fur,
            no_branch=land_wild_no_fur
        )
        
        # Land mammals - Domestic - with fur
        land_domestic_fur = DecisionTreeNode(
            question="Is it a pet (smaller)?",
            yes_branch=dog,
            no_branch=cat
        )
        
        land_domestic_farm = DecisionTreeNode(
            question="Does it moo or neigh?",
            yes_branch=cow,
            no_branch=horse
        )
        
        land_domestic = DecisionTreeNode(
            question="Is it a household pet?",
            yes_branch=land_domestic_fur,
            no_branch=land_domestic_farm
        )
        
        # Land mammals - combined
        land_mammals = DecisionTreeNode(
            question="Is it wild?",
            yes_branch=land_wild,
            no_branch=land_domestic
        )
        
        # Water mammals - with fur
        water_mammals_fur = DecisionTreeNode(
            question="Is it ocean-dwelling (dolphin/whale)?",
            yes_branch=dolphin,
            no_branch=beaver
        )
        
        # Water mammals - combined (all have fur)
        water_mammals = DecisionTreeNode(
            question="Is it fully aquatic or semi-aquatic?",
            yes_branch=water_mammals_fur,
            no_branch=beaver
        )
        
        # All mammals
        mammals = DecisionTreeNode(
            question="Does it live in water?",
            yes_branch=water_mammals,
            no_branch=land_mammals
        )
        
        # Non-mammals - Water animals
        water_non_mammals = DecisionTreeNode(
            question="Is it a fish?",
            yes_branch=shark,
            no_branch=octopus
        )
        
        # Non-mammals - Land animals
        land_non_mammals = DecisionTreeNode(
            question="Does it have wings (bird)?",
            yes_branch=penguin,
            no_branch=ostrich
        )
        
        # Non-mammals - Air animals
        air_non_mammals = DecisionTreeNode(
            question="Does it talk or mimic sounds?",
            yes_branch=parrot,
            no_branch=eagle
        )
        
        # All non-mammals
        non_mammals = DecisionTreeNode(
            question="Where does it live primarily?",
            yes_branch=water_non_mammals,
            no_branch=DecisionTreeNode(
                question="Can it fly well?",
                yes_branch=air_non_mammals,
                no_branch=land_non_mammals
            )
        )
        
        # Root node
        root = DecisionTreeNode(
            question="Is it a mammal?",
            yes_branch=mammals,
            no_branch=non_mammals
        )
        
        return root
    
    def save_tree_to_file(self):
        """Save the current tree to a JSON file."""
        def tree_to_dict(node):
            if node.animal:
                return {"animal": node.animal}
            return {
                "question": node.question,
                "yes": tree_to_dict(node.yes_branch),
                "no": tree_to_dict(node.no_branch)
            }
        
        with open(self.tree_file, 'w') as f:
            json.dump(tree_to_dict(self.root), f, indent=2)
    
    def load_tree_from_file(self):
        """Load tree from JSON file."""
        with open(self.tree_file, 'r') as f:
            data = json.load(f)
        
        def dict_to_tree(node_data):
            if "animal" in node_data:
                return DecisionTreeNode(animal=node_data["animal"])
            return DecisionTreeNode(
                question=node_data["question"],
                yes_branch=dict_to_tree(node_data["yes"]),
                no_branch=dict_to_tree(node_data["no"])
            )
        
        return dict_to_tree(data)
    
    def ask_question(self, question):
        """Ask user a yes/no question and return their answer."""
        while True:
            response = input(f"\n{question} (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer 'yes' or 'no'")
    
    def play(self):
        """Play one round of the game."""
        print("\n" + "="*50)
        print("🎮 ANIMAL GUESSING GAME 🎮")
        print("="*50)
        print("Think of an animal and I'll try to guess it!")
        input("Press Enter when you're ready...")
        
        current_node = self.root
        
        # Traverse the tree
        while current_node.animal is None:
            if current_node.yes_branch is None or current_node.no_branch is None:
                break
            
            if self.ask_question(current_node.question):
                current_node = current_node.yes_branch
            else:
                current_node = current_node.no_branch
        
        # Make the guess
        if current_node.animal:
            print(f"\n🎉 I guess it's a {current_node.animal}!")
            correct = self.ask_question("Did I guess it correctly?")
            
            if correct:
                print("🎊 Excellent! I got it right!")
            else:
                print("\n😅 I was wrong! Help me learn:")
                correct_animal = input("What animal were you thinking of? ").strip()
                distinguishing_question = input(
                    f"What question could distinguish a {correct_animal} from a {current_node.animal}? "
                ).strip()
                answer_for_correct = input(
                    f"For a {correct_animal}, would the answer be yes or no? (yes/no): "
                ).strip().lower() == 'yes'
                
                # Add new animal to tree
                self.add_animal_to_tree(
                    current_node,
                    correct_animal,
                    distinguishing_question,
                    answer_for_correct,
                    current_node.animal
                )
                print("✓ Thank you! I've learned something new!")
                self.save_tree_to_file()
    
    def add_animal_to_tree(self, leaf_node, new_animal, question, answer, old_animal):
        """Add a new animal to the tree at a leaf node."""
        # Create new branches
        if answer:
            # New animal is on yes branch
            leaf_node.yes_branch = DecisionTreeNode(animal=new_animal)
            leaf_node.no_branch = DecisionTreeNode(animal=old_animal)
        else:
            # New animal is on no branch
            leaf_node.yes_branch = DecisionTreeNode(animal=old_animal)
            leaf_node.no_branch = DecisionTreeNode(animal=new_animal)
        
        # Convert leaf to internal node
        leaf_node.question = question
        leaf_node.animal = None
    
    def display_tree(self, node=None, prefix="", is_left=True):
        """Display the tree structure in a readable format."""
        if node is None:
            node = self.root
        
        if node.animal:
            print(f"{prefix}└─ 🦁 {node.animal}")
        else:
            print(f"{prefix}{'└─' if is_left else '├─'} ❓ {node.question}")
            if node.yes_branch:
                print(f"{prefix}│  {'  ' if is_left else '│  '}(Yes)")
                self.display_tree(node.yes_branch, prefix + "│  ", True)
            if node.no_branch:
                print(f"{prefix}{'   ' if is_left else '│  '}(No)")
                self.display_tree(node.no_branch, prefix + "│  ", False)


def main():
    """Main game loop."""
    game = AnimalGuessingGame()
    
    while True:
        print("\n" + "="*50)
        print("What would you like to do?")
        print("1. Play the guessing game")
        print("2. View the decision tree")
        print("3. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            game.play()
        elif choice == '2':
            print("\nCurrent Decision Tree:")
            print("="*50)
            game.display_tree()
        elif choice == '3':
            print("Thanks for playing! Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()