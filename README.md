# Digital Wizards x Hacktoberfest 2024

# Lost and Found Item Matcher

This project aims to automate the matching of lost and found items by utilizing Google Sheets for storing records and comparing visual similarities between items using image processing. The goal is to help participants easily report and find lost items. This project is beginner-friendly and intended for Hacktoberfest participants looking to contribute to open source.

### How It Works

- Users can report lost or found items by filling out a Google Form. The data is stored in a Google Sheet.
- The project uses image processing to match items based on visual similarities.
- If a match is found, the person who reported the lost item will receive an automated email about the found item and the contact information of the finder.

### Key Features

- Uses Google Sheets to store and access data on lost and found items.
- Matches items based on categories, descriptions, and images.
- Sends an automated email to the person who lost an item when a match is found.

## Getting Started

### Prerequisites

- Python 3.x
- Google account to create a service account in Google Cloud
- Libraries: `gspread`, `oauth2client`, `smtplib`, `opencv-python`, `skimage`, `requests`, `numpy`, `matplotlib`, etc.

### Setting Up Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Navigate to **APIs & Services > Credentials** and create a new Service Account.
4. Add a role to your service account, such as **Editor** or **Viewer**.
5. Create a JSON key for your service account, and download it. Save this file as `credSheetsDemo.json` in the root directory of your project.
6. Share the Google Sheets document with your Service Account email address.

For detailed instructions on setting up a Google Cloud Service Account, refer to the [Google Cloud documentation](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).

## How to Get Started 🏁

- Follow the [CONTRIBUTING.md](./CONTRIBUTING.md) file for details.

## Important Dates 🗓️
- There are no dates of submission per say, but the requirement of succesfull Hactoberfest Submission is 4 Succesfull PRs throughout the project.

## Important Note

- To work on the `file.py`, you need to change the `credSheetsDemo.json` file as per the above mentioned steps, and then continue further.
## Our Top Contributors 

<p align="center"><a href="https://github.com/codeclubiittp/HacktoberFest-2024-Lost-and-Found/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=codeclubiittp/HacktoberFest-2024-Lost-and-Found" max={1000} columns={100} anon={1}/>
</a>
   </p>