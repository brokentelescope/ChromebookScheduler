# ChromebookScheduler

Welcome to ChromebookScheduler, an application developed to streamline the process of reserving Chromebooks at Merivale High School. This project was requested by Mr. Gibson in the math department to address specific needs related to Chromebook management and reservation.

## Project Overview and Purpose

ChromebookScheduler is designed to facilitate the reservation and management of Chromebook tubs by teachers. The application satisfies the following requirements:

- **Accessibility:** Teachers must be able to access the application easily.
- **Availability:** Teachers can see which Chromebook tubs are free on which day and during which period.
- **Location Tracking:** Teachers can see where a Chromebook tub is located within the school.
- **Advanced Booking:** Teachers can book Chromebooks at least one month in advance.
- **Cancellation:** Teachers can cancel their bookings and reopen the slot for others.
- **Login System:** A login system for teachers.
- **Activity Log:** A record of who logged out which Chromebook tub, accessible only to Mr. Gibson.

## Installation Instructions

### Prerequisites:
- **Flask Installation:**
  - For Mac users, follow this [YouTube tutorial](https://www.youtube.com/watch?v=B1Qcb5xQ96M).
  - Install Flask using pip: `pip install flask`

### Steps to Run the Application:
1. Clone the GitHub repository: `git clone https://github.com/brokentelescope/ChromebookScheduler`
2. Move the folder into your code editor (e.g., VSCode).
3. Run the `app.py` file.
4. Open the link provided in the terminal in your browser.

## Configuration and Setup

To configure school days and holidays:
1. Locate the `INPUTGOOGLESHEET.txt` file (it should be near the end of the list of names).
2. Follow the instructions in the text file to input data specifying the school day (1/2/3/4) or holiday.

## Usage Instructions

### Account Setup:
1. Sign up for an account.
2. Wait for your account to be verified by the admin.
3. Once verified, you can start reserving Chromebook tubs.

### Booking and Managing Chromebooks:
- View available Chromebook tubs by day and period.
- Book a Chromebook tub for up to one month in advance.
- Cancel your bookings to free up the slot for others.

## Clearing Data

To clear certain data within ChromebookScheduler, follow these steps:

- **Reservation History:**
  - To clear the reservation history, simply click the "Clear History" button on the reservation history page.
  
- **User Database:**
  - To clear the user database, navigate to the admin manage user page. From there, you can edit or delete users as needed.
  
- **Chromebook Database:**
  - To clear the Chromebook database, go to the manage bins section. From there, delete the Chromebook bins that are no longer needed.

## Contributing

We welcome contributions to improve ChromebookScheduler! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Submit a pull request to [this repository](https://github.com/brokentelescope/ChromebookScheduler).

## Tech Stack

The application is built using:
- HTML
- CSS
- JavaScript
- Flask (Python)

## Contact Information

For any questions or support, please reach out to:
- Tianqin Meng: tianqin.steven.meng@gmail.com
- Owen Chen: ochen2@ocdsb.ca

## Contributors

This project was developed by Owen Chen, Tianqin Meng, and Rex Li from Merivale High School.
