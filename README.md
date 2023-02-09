# EEB2 reunion

## Table of content
- [About the project](#about-the-project)
  * Screenshots
  * Tech Stack
  * Features
  * Environment Variables
- Getting started
  * Prerequisits
  * Run locally
  * Deployment 
  * Other commands
- Roadmap
- Contributing 
- FAQ
- License 
- Contact
- Acknowledgements


## About the Project
In 2025, it will be 20 years since we graduated from high school. This calls for celebrations!

Some people started getting people together via a WhatsApp group, and this made me realise that we might need a more robust way of managing the RSVPs. We have all the names of the students in the Bac Book, all we are missing is their contact details, to reach out. 

This platform aims to:
1. Spread the word about the event.
2. Help collect contact details of past classmates.


### Screenshots
<img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />

### Tech Stack

<details>
  <summary>Web app</summary>
  <ul>
    <li><a href="https://www.typescriptlang.org/](https://flask.palletsprojects.com/en/2.2.x/">Python Flask</a></li>
    <li><a href="https://getbootstrap.com/docs/3.4/css/">Bootstrap CSS</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

### Features

- Homepage
  - Information about the event
  - Count of guest list / users / RSVPs
  - Share (on Facebook, Instagram, email, etc.)
  - Invite to the WhatsApp group
- Signup
  - Map users to members of the guest list
- Reset password 
- Login 
- RSVP / Payment 
- Spread the word
  - Help identify missing members of the guest list and invite them to use the platform
  - Invite users who are not members of the guest list (teachers, people who failed years, etc)
- Administration
  - Guest list management
  - User / RSVP management
- Contact us

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file.

```bash

```

## Getting Started

### Prerequisites

This project uses Yarn as package manager

```bash

```

### Run Locally

Clone the project

```bash
  git clone https://github.com/to-ie/eeb2-reunion
```

Go to the project directory

```bash
  cd eeb2-reunion
```

Install dependencies

```bash

```

Start the server

```bash

```

### Deployment

To deploy this project run

```bash

```

### Other commands

```bash

```

## Roadmap
* [ ] Create the signup / login mechanism 
  * [ ] Create signup / login / password reset module 
    * [ ] Once a user signsup, map user to guest in the guest list.
    * [ ] Then redirect user to 'Spread the word page'. 
    * [ ] Make sure signup module is not subject to script injections  / explore AWS Cognito 
  * [ ] Create the login module 
    * [ ] User categories: Admin / View only / Student / Other
    * [ ] If the user is not already linked to a member of the guest list, ask the user to identify themselves. 
* [ ] Create the header/menu structure with all pages (blank)
  * [ ] Homepage
    * [ ] Information about the event 
    * [ ] Count of guest list / users / RSVPs
    * [ ] Share (on Facebook, Instagram, email, etc.)
    * [ ] Invite to the WhatsApp group
  * [ ] About the event
  * [ ] RSVP / Payment
    * [ ] Make sure the user is mapped to a guest in the guest list. If not, redirect to the right page 
    * [ ] Allow user to tentatively confirm presence by tick-box
    * [ ] Allow user to confirm the presence by payment.
    * [ ] [?] Allow +1s? How to manage additional guests?
* [ ] Spread the word
  * [ ] Show a list of guests that are not currently registered and allow user to send an email invite. 
  * [ ] Allow user to send an invitation to users who are not part of the guest list (teachers, students who failed the previous year).
  * [ ] Get in touch if the guest list is incomplete. 
* [ ] Administration
  * [ ] Guest list management
    * [ ] Creation of new groups (class section, teacher, failed class, other) in the guest list 
    * [ ] Creation of new guests in the guest list 
    * [ ] Removal of guests in the guest list 
  * [ ] User / RSVP / Payment management 
    * [ ] Lists of users who have registered / RSVP'd / Paid
* [ ] Contact us
    * [ ] Contact form

**Other:** 
* [ ] Organise the event (who?)

## Contributing

Contributions are always welcome! Get in touch if you are not sure how you can help! 

If you want to help out with the technical side of this project, pull requests are the simplest way.

## FAQ

- Why?
  + It will be 20 years since we graduated, surely it's important to mark the day?

## License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/).

## Contact

Theo - toie@duck.com

## Acknowledgements

Useful resources and libraries that we have used in this project:

 - [Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template)


