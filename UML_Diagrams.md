# Virtual Pet Simulator - UML Diagrams

This document contains the professional UML diagrams for the Virtual Pet Simulator application. They are written using [Mermaid.js](https://mermaid.js.org/) syntax, which allows them to render automatically in GitHub, VS Code, and other modern Markdown viewers. 

> **Note on exporting to images:** To export these as high-quality PNG or SVG images, you can paste the code blocks into the [Mermaid Live Editor](https://mermaid.live/), which has a built-in "Export Image" feature.

---

## 1. Use Case Diagram
This diagram shows the system from the User's perspective, mapping out all the actions they can perform.

```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam linetype ortho

skinparam usecase {
    BackgroundColor white
    BorderColor black
}
skinparam actor {
    BackgroundColor white
    BorderColor black
}
skinparam rectangle {
    BackgroundColor transparent
    BorderColor black
    BorderThickness 2
}

left to right direction

actor "User" as user

rectangle "Virtual Pet Simulator System" {
  usecase "Feed Pet" as feed
  usecase "Play with Pet" as play
  usecase "Put Pet to Sleep" as sleep
  usecase "View Pet Status" as view
  usecase "Save Game" as save
  usecase "Load Game" as load
  usecase "Restart Game" as restart
  usecase "Exit Application" as exit
}

user --> feed
user --> play
user --> sleep
user --> view
user --> save
user --> load
user --> restart
user --> exit

feed --> view
play --> view
sleep --> view
@enduml
```

---

## 2. Class Diagram
This diagram breaks down the system into objects/classes, detailing their attributes, methods, and relationships.

```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam linetype ortho

skinparam class {
    BackgroundColor white
    BorderColor black
    ArrowColor black
}

class VirtualPet {
  + hunger : int
  + happiness : int
  + energy : int
  + mood : String
  + name : String
  + feed()
  + play()
  + sleep()
  + update_mood()
}

class PetGUI {
  + main_window : Object
  + labels : List
  + buttons : List
  + progress_bars : List
  + create_widgets()
  + update_display()
  + show_message()
}

class FileManager {
  + save_data()
  + load_data()
}

PetGUI --> VirtualPet : Interacts with
PetGUI --> FileManager : Uses
@enduml
```

---

## 3. Activity Diagram
This diagram models the dynamic behavior and flow of the program from initialization to exit.

```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam linetype ortho

skinparam state {
    BackgroundColor white
    BorderColor black
}

[*] --> StartApplication
StartApplication --> LoadGameData
LoadGameData --> DisplayGUI
DisplayGUI --> UserSelectsAction

UserSelectsAction --> UpdatePetStats : User Performs Action
UpdatePetStats --> UpdateMood
UpdateMood --> SaveData
SaveData --> CheckGameOver

CheckGameOver --> DisplayGUI : Game Continues
CheckGameOver --> GameOverState : Hunger=100 & Happiness=0
GameOverState --> RestartGame : User clicks Restart
RestartGame --> DisplayGUI

UserSelectsAction --> ExitApplication : User clicks Exit
GameOverState --> ExitApplication : User clicks Exit
ExitApplication --> [*]
@enduml
```

---

## 4. Sequence Diagram
This diagram shows the exact interaction order between the User, GUI, Pet Logic, and File System over time when a button is clicked.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "#ffffff", "primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "lineColor": "#000000", "actorBkg": "#ffffff", "actorBorder": "#000000", "actorTextColor": "#000000", "signalColor": "#000000", "activationBkgColor": "#d1d5db", "activationBorderColor": "#000000"}}}%%
sequenceDiagram
    actor User
    participant GUI
    participant VirtualPet
    participant FileManager

    User->>GUI: 1. Clicks "Feed Pet" button
    activate GUI
    Note over GUI: 2. GUI receives button event
    
    GUI->>VirtualPet: 3. Sends feed() request
    activate VirtualPet
    Note over VirtualPet: 4. VirtualPet updates hunger value
    VirtualPet-->>GUI: 5. Returns updated stats
    deactivate VirtualPet
    
    Note over GUI: 6. Refreshes pet status labels/progress bars
    
    GUI->>FileManager: 7. Sends save_data() request
    activate FileManager
    Note over FileManager: 8. FileManager stores updated pet data
    FileManager-->>GUI: Data successfully stored
    deactivate FileManager
    
    GUI-->>User: 9. Displays updated values to the User
    deactivate GUI
```

---

## 5. State Diagram
This diagram focuses on the Virtual Pet's states (moods) and how it transitions from one to another based on its stats.

```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam linetype ortho

skinparam nodesep 100
skinparam ranksep 100

skinparam state {
    BackgroundColor white
    BorderColor black
}

state "Game Over" as GameOver

[*] --> Happy : Start Game

Happy --> Hungry : Hunger increasing
Hungry -up-> Happy : Feeding

Happy --> Excited : Playing

Happy -left-> Sleepy : Low energy
Sleepy -right-> Happy : Sleeping

Hungry --> GameOver : Hunger reaching max
Excited --> GameOver : Happiness reaching zero

GameOver -up-> Happy : Restart button
GameOver --> [*] : Exit Application
@enduml
```
