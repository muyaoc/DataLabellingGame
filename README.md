# Data Labelling Game Framework and Simulation



When starting the application, you will be prompted to either create a new task or join an existing task.

- If you create a new task, you start a new game as the host. In this role, you set a new unique task id and upload the dataset that you want to be labelled. Since this application is a simulation, the existing test dataset is used and the application has no further function here.

- If you join an existing task, you then need to enter the task id for an existing task. We are using the given test dataset, so the input here is ignored and the test dataset is loaded. You are then prompted to select the role you want to join as.

You will "join" an existing task as either a Packer, Labeller, Guesser or Reviewer.

- **Packer**: the raw images will open in a new window and you can drag across the image to create separate bounding boxes for objects. The following hotkeys are available:

    `S` : Save current bounding boxes as an entry in the .csv file.

    `C` : cancel current bounding boxes

    `N` : save all selected bounding boxes as separate entries in the .csv file, and move to next image

    `Q` : move to next image without saving

- **Labeller**: the bounding boxes created by a packer are displayed one at a time.

    `0 - x` : Select a corresponding label for the rectangle (out of x - 1 possible label choices). The entry in the .csv file has the label appended to it.

- **Guesser**: the bounding boxes created by a packer and labelled by a labeller are displayed one at a time without the label.

    `0 - 2` : When labelled correctly, no action is done and we move to the next rectangle. When labelled incorrectly, the label for the rectangle will be overwritten, and the entry in the .csv file has a "*" appended to it.

    `;` : This key is to be used when the guesser does not agree with any of the provided labels. The entry in the .csv file will have "*" appended to it without altering the existing label.

- **Reviewer**: the bounding boxes created by a packer and labelled by a labeller are displayed for review.

    `1` : Accept the label. The entry in the .csv has its asterisks cleared.
    
    `0` : Reject the label. The entry in the .csv has its label and asterisks cleared.

    `;` : Reject the bounding box selection. The entry in the .csv is deleted.