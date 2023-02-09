# EEB2 reunion

## About the Project

This project aims to facilitate the organisation of our 20-year anniversary since we graduated from high school. Since we are dealing with many students scattered all around the globe, we need a mechanism to collect contact details for everyone, in order to invite them to the event. 

### Screenshots
<img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />

### Tech Stack

<details>
  <summary>Client</summary>
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

To run this project, you will need to add the following environment variables to your .env file
[TBC]

## Getting Started

### Prerequisites

This project uses Yarn as package manager

```bash
 npm install --global yarn
```

### Run Locally

Clone the project

```bash
  git clone [github ULR]
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  yarn install
```

Start the server

```bash
  yarn start
```

### Deployment

To deploy this project run

```bash
  yarn deploy
```

## Roadmap
* [ ] Create the signup / login mechanism 
	* [ ] Create the login module 
	  * [ ] If the user is not already linked to a member of the guest list, ask the user to identify themselves. 
	* [ ] Create signup / login / password reset module 
	  * [ ] Link signup of user to guest in the guest list 
	  * [ ] Make sure signup module is not subject to script injections 
	  * [ ] Explore AWS Cognito 
* [ ] Create the header/menu structure with all pages (blank)
  * [ ] Homepage
    * [ ] Information about the event 
    * [ ] Count of guest list / users / RSVPs
    * [ ] Invite to the WhatsApp group
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

Other: 
* [ ] Organise the event 

## Contributing

Contributions are always welcome! PRs are the simplest way. 

## FAQ

- Why?
  + It will be 20 years since we graduated, surely it's important to mark the day?

- Question 2
  + Answer 2

## License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/).

## Contact

Theo - toie@duck.com

## Acknowledgements

Useful resources and libraries that we have used in this project:

 - [Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template)


