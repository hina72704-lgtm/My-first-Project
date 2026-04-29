import json
import os
import re
from datetime import datetime

# File to store contacts
DATA_FILE = "contacts.json"

def load_contacts():
    """Load contacts from JSON file"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(" Error reading file. Starting with empty contacts.")
        return {}

def save_contacts(contacts):
    """Save contacts to JSON file"""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(contacts, file, indent=4)
        return True
    except Exception as e:
        print(f" Error saving contacts: {e}")
        return False

def validate_email(email):
    """Professional email validation"""
    # Regular expression for valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def validate_phone(phone):
    """Professional phone validation"""
    # Remove any spaces or special characters
    phone = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Check if it's digits only and length between 10-15
    return phone.isdigit() and 10 <= len(phone) <= 15

def get_next_id(contacts):
    """Generate next unique ID"""
    if not contacts:
        return 1
    return max(int(id) for id in contacts.keys()) + 1

def add_contact(contacts):
    """Add a new contact with better error handling"""
    print("\n" + "="*50)
    print("ADD NEW CONTACT")
    print("="*50)
    
    # Get Name
    while True:
        name = input("Full Name: ").strip()
        if not name:
            print(" ERROR: Name cannot be empty! Please try again.")
        elif len(name) < 2:
            print(" ERROR: Name must be at least 2 characters! Please try again.")
        else:
            break
    
    # Get Phone with validation loop
    while True:
        phone = input("Phone Number: ").strip()
        if not phone:
            print(" ERROR: Phone number cannot be empty! Please try again.")
        elif not validate_phone(phone):
            print(" ERROR: Invalid phone number! Use 10-15 digits only (e.g., 03001234567)")
            print("   Special characters like +, -, () are not allowed.")
        else:
            # Clean the phone number
            phone = re.sub(r'[\s\-\(\)\+]', '', phone)
            break
    
    # Get Email with validation loop
    while True:
        email = input("Email Address: ").strip()
        if not email:
            print(" ERROR: Email cannot be empty! Please try again.")
        elif not validate_email(email):
            print(" ERROR: Invalid email format! Example: name@domain.com")
            print("   Email must contain @ and a valid domain (e.g., .com, .org)")
        else:
            break
    
    # Get City
    while True:
        city = input("City: ").strip()
        if not city:
            print(" ERROR: City cannot be empty! Please try again.")
        else:
            break
    
    # Get Company
    while True:
        company = input("Company: ").strip()
        if not company:
            print(" ERROR: Company cannot be empty! Please try again.")
        else:
            break
    
    # Create new contact
    contact_id = get_next_id(contacts)
    contacts[str(contact_id)] = {
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if save_contacts(contacts):
        print(f"\n✅ Contact added successfully! (ID: {contact_id})")
        print(f"   {name} | {phone} | {email}")
    else:
        print(" Failed to save contact!")

def display_contacts(contacts, title="CONTACTS LIST"):
    """Display contacts in a formatted table"""
    if not contacts:
        print("\n📭 No contacts found!")
        return False
    
    print("\n" + "="*110)
    print(f"{title:^110}")
    print("="*110)
    print(f"{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<30} {'City':<15} {'Company':<15}")
    print("-"*110)
    
    for contact_id, contact in contacts.items():
        # Truncate long emails if needed
        email_display = contact['email'][:28] + ".." if len(contact['email']) > 30 else contact['email']
        print(f"{contact_id:<5} {contact['name']:<20} {contact['phone']:<15} "
              f"{email_display:<30} {contact['city']:<15} {contact['company']:<15}")
    
    print("="*110)
    print(f"📊 Total: {len(contacts)} contacts")
    return True

def search_contacts(contacts):
    """Search contacts by name, phone, or email"""
    if not contacts:
        print("\n📭 No contacts to search!")
        return
    
    print("\n" + "="*50)
    print("SEARCH CONTACTS")
    print("="*50)
    print("1. Search by Name")
    print("2. Search by Phone")
    print("3. Search by Email")
    
    while True:
        choice = input("\nChoose option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print(" ERROR: Invalid choice! Please enter 1, 2, or 3.")
    
    search_term = input("Enter search term: ").strip().lower()
    if not search_term:
        print(" ERROR: Search term cannot be empty!")
        return
    
    results = {}
    
    for contact_id, contact in contacts.items():
        if choice == "1" and search_term in contact['name'].lower():
            results[contact_id] = contact
        elif choice == "2" and search_term == contact['phone']:
            results[contact_id] = contact
        elif choice == "3" and search_term in contact['email'].lower():
            results[contact_id] = contact
    
    if results:
        display_contacts(results, f"🔍 SEARCH RESULTS: '{search_term}'")
    else:
        print(f"\n No contacts found matching '{search_term}'")

def filter_contacts(contacts):
    """Filter contacts by city or company"""
    if not contacts:
        print("\n📭 No contacts to filter!")
        return
    
    print("\n" + "="*50)
    print("FILTER CONTACTS")
    print("="*50)
    print("1. Filter by City")
    print("2. Filter by Company")
    
    while True:
        choice = input("\nChoose option (1-2): ").strip()
        if choice in ["1", "2"]:
            break
        print(" ERROR: Invalid choice! Please enter 1 or 2.")
    
    filter_value = input(f"Enter {'city' if choice == '1' else 'company'} name: ").strip().lower()
    if not filter_value:
        print(" ERROR: Filter value cannot be empty!")
        return
    
    results = {}
    filter_by = 'city' if choice == '1' else 'company'
    
    for contact_id, contact in contacts.items():
        if filter_value == contact[filter_by].lower():
            results[contact_id] = contact
    
    if results:
        display_contacts(results, f" FILTERED BY {filter_by.upper()}: '{filter_value}'")
    else:
        print(f"\n No contacts found with {filter_by} = '{filter_value}'")

def update_contact(contacts):
    """Update an existing contact with validation"""
    if not contacts:
        print("\n No contacts to update!")
        return
    
    display_contacts(contacts)
    
    while True:
        contact_id = input("\nEnter Contact ID to update: ").strip()
        if contact_id in contacts:
            break
        print(f" ERROR: Contact ID '{contact_id}' not found! Please enter a valid ID.")
    
    contact = contacts[contact_id]
    print(f"\n Updating: {contact['name']} (ID: {contact_id})")
    print("Leave field empty to keep current value\n")
    
    # Update Name
    new_name = input(f"Name [{contact['name']}]: ").strip()
    if new_name:
        if len(new_name) >= 2:
            contact['name'] = new_name
        else:
            print(" Name too short! Keeping old value.")
    
    # Update Phone with validation
    new_phone = input(f"Phone [{contact['phone']}]: ").strip()
    if new_phone:
        if validate_phone(new_phone):
            contact['phone'] = re.sub(r'[\s\-\(\)\+]', '', new_phone)
        else:
            print(" Invalid phone format! Keeping old value.")
    
    # Update Email with validation
    new_email = input(f"Email [{contact['email']}]: ").strip()
    if new_email:
        if validate_email(new_email):
            contact['email'] = new_email
        else:
            print(" Invalid email format! Keeping old value.")
    
    # Update City
    new_city = input(f"City [{contact['city']}]: ").strip()
    if new_city:
        contact['city'] = new_city
    
    # Update Company
    new_company = input(f"Company [{contact['company']}]: ").strip()
    if new_company:
        contact['company'] = new_company
    
    contacts[contact_id] = contact
    
    if save_contacts(contacts):
        print(f"\n Contact updated successfully!")
        print(f"   {contact['name']} | {contact['phone']} | {contact['email']}")
    else:
        print(" Failed to update contact!")

def delete_contact(contacts):
    """Delete a contact with confirmation"""
    if not contacts:
        print("\n📭 No contacts to delete!")
        return
    
    display_contacts(contacts)
    
    while True:
        contact_id = input("\nEnter Contact ID to delete: ").strip()
        if contact_id in contacts:
            break
        print(f" ERROR: Contact ID '{contact_id}' not found! Please enter a valid ID.")
    
    # Confirm deletion
    print(f"\n  WARNING: You are about to delete '{contacts[contact_id]['name']}'")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        deleted_name = contacts[contact_id]['name']
        del contacts[contact_id]
        
        if save_contacts(contacts):
            print(f" Contact '{deleted_name}' deleted successfully!")
        else:
            print(" Failed to delete!")
    else:
        print(" Deletion cancelled.")

def main():
    """Main menu-driven interface"""
    print("\n" + "="*50)
    print(" WELCOME TO CONTACT MANAGEMENT SYSTEM")
    print("="*50)
    
    contacts = load_contacts()
    print(f"✅ Loaded {len(contacts)} existing contacts")
    
    while True:
        print("\n" + "="*50)
        print(" CONTACT MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add Contact")
        print("2.  View All Contacts")
        print("3.  Search Contacts")
        print("4.  Filter Contacts")
        print("5.  Update Contact")
        print("6.  Delete Contact")
        print("7.  Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_contact(contacts)
            contacts = load_contacts()
        
        elif choice == "2":
            display_contacts(contacts)
        
        elif choice == "3":
            search_contacts(contacts)
        
        elif choice == "4":
            filter_contacts(contacts)
        
        elif choice == "5":
            update_contact(contacts)
            contacts = load_contacts()
        
        elif choice == "6":
            delete_contact(contacts)
            contacts = load_contacts()
        
        elif choice == "7":
            print("\n👋 Goodbye! Thanks for using Contact Manager.")
            print(f"📁 Your contacts are saved in '{DATA_FILE}'")
            break
        
        else:
            print(" ERROR: Invalid choice! Please enter a number between 1 and 7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()