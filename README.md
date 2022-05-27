# Data Labelling Game Framework and Simulation

The artefact includes:
- code for game frameworks
- code for simulation of the game process
- and the design of the game interface and visual prototype. (More details for the prototype type can be found [here](prototypes/README.md))


## Run the simulation
From the root folder, simply run `python main.py` in the terminal to start the application.

You will be prompted to either create a new task or join an existing task.

- If you create a new task, you start a new game as the host. In this role, you set a new unique task id and upload the dataset that you want to be labelled. Since this application is a simulation, the existing [test dataset](test_dataset) is used and the application has no further function here.

- If you join an existing task, you then need to enter the task id for an existing task. We are using the given test dataset, so the input here is ignored and the test dataset is loaded. You are then prompted to select the role you want to join as.

- Since the task id is not saved in the server, the task id is forced to be "test". The Packer, Labeller, Guesser and Reviewer can only work on `test.csv`.

- The output file can be viewed in the `tasks/test/test.csv`


You will "join" an existing task as either a Packer, Labeller, Guesser or Reviewer.

- **Packer**: the raw images will open in a new window and you can drag across the image to create separate bounding boxes for objects. The following hotkeys are available:

    `S` : save current bounding boxes as an entry in the .csv file.

    `C` : cancel current bounding boxes

    `N` : save all selected bounding boxes as separate entries in the .csv file, and move to next image

    `Q` : move to next image without saving

- **Labeller**: the bounding boxes created by a packer are displayed one at a time.

    `0 - x` : Select a corresponding label for the rectangle (out of x - 1 possible label choices). The entry in the .csv file has the label appended to it.

- **Guesser**: the bounding boxes created by a packer and labelled by a labeller are displayed one at a time without the label.

    `0 - 2` : When labelled correctly, no action is done and we move to the next rectangle. When labelled incorrectly, a copy of the existing entry, with the guesser's new label (and the asterisk will be appended to both labels), will be added to the .csv.

    `;` : This key is to be used when the guesser does not agree with any of the provided labels. The entry in the .csv file will have "*" appended to it without altering the existing label.

- **Reviewer**: the bounding boxes created by a packer and labelled by a labeller are displayed for review.

    `1` : Accept the label. If the label are flagged with "*", its asterisk will be cleared.
    
    `0` : Reject the label. The label will be removed (be replaced by `np.NaN`) for that entry.

    `;` : Reject the bounding box selection. The entry in the .csv is deleted.


## Dataset

The fruit dataset currently used is a mixed selection of images of fruits. These images have been sourced from:

- https://www.kaggle.com/datasets/moltean/fruits

- https://www.kaggle.com/datasets/mbkinaci/fruit-images-for-object-detection

However, the program might perform as unintended due to large image size.

Another datasets with smaller image size are considered to used for testing purpose. These images have been sourced from:
** selfies with sunglasses:
- https://github.com/shreyas0906/Selfies-with-sunglasses

## Framework
The class files contained in the folder [frameworks](frameworks) demonstrate how each player client would communicate its data to a server and vice versa. Each player would call the `listen()` function in a waiting loop and respond to messages received from the server and act accordingly.

## The Design of User Interface
The prototype of the user interface can be found [here](prototypes)