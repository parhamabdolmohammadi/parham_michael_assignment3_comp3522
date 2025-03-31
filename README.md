# 🧠 Async Pokédex Application

**Authors:**  
Michael McBride (A01394787)  
Parham Abdolmohammadi (A01356970)    

## 📌 Overview

This is an **asynchronous, object-oriented Pokédex application** developed for COMP3522 Assignment 3. The application retrieves and displays detailed Pokémon-related data—such as Pokémon, moves, abilities, and stats—by querying the [PokéAPI](https://pokeapi.co/) asynchronously using aiohttp and asyncio.

## ✅ Features

- ✅ Supports **Pokemon**, **Ability**, and **Move** queries  
- ✅ Input data from a file or command-line  
- ✅ Option to retrieve **expanded** information (i.e., deeper data from related endpoints)  
- ✅ Outputs results to the **console** or an **output file**  
- ✅ Follows **SOLID principles** and **abstract base class** design patterns  
- ✅ Built using **asynchronous programming** for concurrent API calls

## 📂 Project Structure

```bash
.
├── main.py                 # Entry point, handles CLI & runs the app
├── request.py              # Defines the Request class
├── pokedex_object.py       # Contains domain models (Pokemon, Move, Stat, Ability)
├── retriever.py            # Abstract base class + all retriever subclasses
├── retrieverFacade.py      # Facade to delegate request execution
└── requirements.txt        # (Optional) Required libraries
```

## 🧪 Usage

## 🧾 Command-line Arguments
python main.py <mode> (--inputfile FILE.txt | --inputdata NAME_OR_ID) [--expanded] [--output OUTPUT.txt]

## 🔍 Examples

### Retrieve basic info for Pikachu
python main.py pokemon --inputdata pikachu

### Retrieve expanded info for multiple moves from a file
python main.py move --inputfile moves.txt --expanded

### Retrieve an ability and write output to a file
python main.py ability --inputdata overgrow --output output.txt

# 📄 Input File Format
pikachu
bulbasaur
charizard

# ⚙️ Requirements
Python 3.10+

aiohttp


# Install dependencies:
pip install aiohttp

# 💡 Design Principles
Async/Await: Efficient API handling with concurrent fetches

Open/Closed Principle: New retrievers can be added easily by extending the Retriever base class

Facade Pattern: Simplified interface for running requests via PokedexRetrieverFacade

Encapsulation: Domain objects hide internal attributes with property access

# 📫 Contact
For questions or suggestions, feel free to reach out via GitHub or email the authors.  do it again exact same


