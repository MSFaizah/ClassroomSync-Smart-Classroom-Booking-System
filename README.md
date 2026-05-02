# 🏫 ClassroomSync — Smart Classroom Booking System
ClassroomSync is a Django-based web application that streamlines classroom booking and management. Admins can manage rooms, publish alerts, and handle requests, while students view real-time availability and book rooms. The system also features dynamic alerts with auto-expiry, ensuring efficient communication and conflict-free scheduling.

## 📌 Problem Statement
In many colleges, classroom allocation and booking are handled manually or through unstructured systems. This leads to:
* ❌ Double bookings and scheduling conflicts
* ❌ Lack of real-time room availability visibility
* ❌ Inefficient communication of notices (holidays, maintenance, exam blocks)
* ❌ No centralized system for admin control and student requests
**ClassroomSync** solves this by providing a **centralized, real-time classroom booking and alert management system**.

## 🎯 Objective
To build a **web-based platform** that allows:
* Admins to manage rooms, bookings, and alerts
* Students to check availability and request bookings
* Real-time visibility of classroom status


## ⚙️ Core Modules (Functionality)

### 👨‍💼 1. Admin Module
* Secure login using Django Authentication
* Publish alerts:
  * 🚫 Booking Blocks
  * 📅 Notices
  * ℹ️ Information
* Manage classrooms
* Approve / reject booking requests
* Manual room booking & cancellation
* Delete alerts (❌ option)
* Auto-expiring alerts based on time


### 👩‍🎓 2. Student Module
* View available classrooms in real-time
* Check room status:
  * ✅ Available
  * ❌ Booked
  * 🚫 Blocked
* Send booking requests
* View live alerts from admin dashboard


### 🚨 3. Alert System 
* Alerts displayed across **Admin & Student dashboards**
* Types:
  * Booking Block
  * Notice
  * Information
* Auto-expiry system:
  * Alerts disappear after end time
  * Smooth UI fade-out effect
* Backend cleanup of expired alerts


### 🏫 4. Classroom Management
* Room listing and categorization (floors/departments)
* Grid-based UI for quick visualization
* Real-time availability updates


### 📬 5. Booking System
* Request-based booking flow
* Admin approval/rejection
* Time-based validation
* Prevents overlapping bookings

### 🔐 6. Authentication System
* Built using Django’s built-in authentication
* Role-based access (Admin / Student)

## 🧱 Tech Stack
| Layer             | Technology Used                  | Purpose                                                   |
| ----------------- | -------------------------------- | --------------------------------------------------------- |
| 🖥️ Frontend      | HTML5, CSS, JavaScript            | Structure of web pages and interactivity                  |
| ⚙️ Backend        | Python                           | Core programming language                                 |
|                   | Django                           | Web framework for handling logic, routing, authentication  |
| 🗄️ Database      | MySQL                            | Storing rooms, bookings, alerts, users                     |
| 🔗 ORM            | Django ORM                       | Database interaction using Python models                  |
| 🔐 Authentication | Django Auth System               | Login, logout, session management                         |
| 🛠️ Tools         | Git & GitHub                     | Version control and project hosting                        |

## 🎥 Project Demo

📽️ *Watch the working demo of ClassroomSync below:*

> *(Will soon upload here)*


## ✨ Key Features

* 🔄 Real-time classroom availability
* 🚨 Cross-dashboard alert system
* ⏳ Auto-expiring alerts with smooth UI transitions
* 📊 Clean and responsive UI design
* 🔐 Secure authentication system
* ⚡ Scalable architecture using Django

## 🚀 Future Enhancements
* 📱 Mobile responsive PWA version
* 📊 Analytics dashboard for room usage
* 🤖 Smart room recommendation system (AI-based)
* 📅 Calendar integration (Google Calendar)


## 🧠 Learning Outcomes
* Full-stack development using Django
* Database design & relationships
* Real-time UI updates
* System design thinking
* Debugging real-world issues


## 📌 Conclusion

ClassroomSync transforms traditional classroom booking into a **smart, efficient, and automated system**, reducing manual effort and improving resource utilization in educational institutions.

## 👩‍💻 Author
**MSFaizah**
BSc IT | Aspiring Data Scientist & Full Stack Developer
