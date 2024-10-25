# Workio

**Workio** is a web platform designed to streamline project management and enhance team collaboration. With features for creating boards, lists, and cards, teams can organize tasks effectively, set priorities, and manage project workflows in a user-friendly environment.

---

## Main Features

- **User Authentication**: Secure user registration and login.
- **Task Organization**: Create boards, lists, and cards to organize and track tasks.
- **Role-Based Permissions**: 
  - **Admins**: Manage lists and cards, edit cards, and view member details.
  - **Members**: View, and set priorities and statuses.
  

---
## Features Details:

### User Management
- **User Registration**: New users can register an account via a registration link.
- **User Login**: Existing users can log in using their credentials.

### Board, List, and Card Management
- **Create Board**: Users can create a board.
- **Board Details**: Users can add members to a board and create lists.
- **Add to Card**: Users can add cards to the lists.

### Card Management
- **Card Priority**: The board admin and added members can prioritize the card.
- **Card Status**: Both the board admin and added members can set the card's status.

### Add Member Management
- **View Board**: Added members can view the board.
- **View List**: Added members can view the lists within the board.
- **Edit and Delete a Card**: Added members can view, edit, and delete cards.

### Board Admin Management
- **Edit and Delete**: Admins can edit and delete lists and cards.
- **View Board Member Details**: Admins can view details of every board member.
- **View Total Boards and Members**: Admins can view all boards and all members.
## Technologies Used

## API Endpoints

### User Management
- **POST** `/api/account/register/` - Register a new user.
- **POST** `/api/account/login/` - User login.

### Board Management
- **GET** `/api/board/board/` - List all boards.
- **GET** `/api/board/board/{id}/` - Retrieve a specific board’s details.

### List Management
- **GET** `/api/board/list/` - Retrieve all lists within boards.
- **POST** `/api/board/list/` - Add a new list.
- **PUT** `/api/board/{board_id}/list/{list_id}/` - Update a specific list.
- **DELETE** `/api/board/{board_id}/list/{list_id}/` - Delete a specific list.

### Card Management
- **GET** `/api/board/card/` - Retrieve all cards.
- **POST** `/api/board/list/{list_id}/card/` - Add a new card to a list.
- **PUT** `/api/board/card/{card_id}/` - Update a specific card.
- **DELETE** `/api/board/card/{card_id}/` - Delete a specific card.

### Member Management
- **POST** `/api/board/{board_id}/addmember/` - Add a new member to a board.
- **GET** `/api/board/member/{board_id}/` - Retrieve members of a board.

---
## Technologies Used

### Backend
- **Python 3.x**: Programming language.
- **Django**: Web framework for backend development.
- **Django REST Framework**: API development for seamless frontend-backend communication.

---

## Live Demo

- **Frontend**: [Workio Frontend](https://amenaakterkeya.github.io/workio./index.html)
- **Backend**: [Workio Backend](https://workio-theta.vercel.app/)

---
## Installation & Running the App

### Prerequisites
- **Python 3.x**
- **Django** and **Django REST Framework**

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/workio.git
   cd workio
2. **Install Dependencies:**:
   ```bash
   pip install -r requirements.txt
3. **Run Database Migrations:**:
   ```bash
   python manage.py migrate
4. **Start the Development Server:**:
   ```bash
   python manage.py runserver
5. **Run Tests:**:
   ```bash
   python manage.py test
The backend server will be accessible at http://localhost:8000/api/.

## License

This project is licensed under the MIT License.
This version includes all information within a single structured flow in `README.md`. It’s designed for easy access and readability for anyone interacting with the repository.
