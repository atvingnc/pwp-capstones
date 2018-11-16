##
## TomeRater project :
## application to keep track of readers and their books.
##
## Phillip Jerzak - Code Academy - Programming with Python
##
## Program written and debugged with Pycharm Edu 2018.2
##

## TomeRater class - allows creation and maintenence of User/Book objects. this is the top
## level access into User objects
class TomeRater():

    def __init__(self):
        self.users = {}  ## email -> User object
        self.books = {}  ## Book object -> number users that have read it

    ## create generic book oject
    def create_book(self, title, isbn):
        return Book(title, isbn)

    ## create novel book object
    def create_novel(self, title, author, isbn):
         return Fiction(title, author, isbn)

    ## create non-fiction book object
    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    ## add a book to the User object
    def add_book_to_user(self, book, email, rating = None):
        ## if email key doesn't exist then print a message for the user
        if(email in self.users): ## is there an email key
            ## before we add it to the user and TomeRater dict., does this book have a unique ISBN
            for key in self.books.keys(): ## get each book object
                if((key.title != book.title) and (key.isbn == book.isbn)):
                    print("ISBN for", book,  "is the same as", key, "\n\r")
                    return

            user = self.users[email]  ## get the User object
            user.read_book(book, rating) ## call read_book in User object

            ## set rating if there is a valid one
            if(rating != None):
                book.add_rating(rating)

            if(book in self.books):  ## is the book already in the dictionary
                value = self.books[book]  ## retrieve the number times read
                value = value + 1
                self.books[book] = value ## put new number back
            else:
                self.books[book] = 1
        else:  # user is not in dictionary, print message
            print("No user with that email: ", email)


    ## add new User object
    def add_user(self, name, email, user_books = None):
        if(email in self.users): ## is there an email key
            print("\n\rUser already exists: ", email, "\n\r")
        else:
            if(('@' in email) and ((".com" in email) or (".edu" in email) or (".org" in email))):
                new_user = User(name, email)
                self.users[email] = new_user
                if(user_books != None):
                    for book in user_books:
                        self.add_book_to_user(book, email, rating = None)
            else:
                print("\n\rInvalid email address: ", email, "\n\r")

    def print_catalog(self):
        print("\n\r======= Book Catalog: =======")
        for book in self.books:
            print("- ", book)
        print("\n\r")

    def print_users(self):
        print("\n\r======= User List: =======")
        for user in self.users:
            print("- ", user)
        print("\n\r")

    def most_read_book(self):
        most_read_key = ""
        most_read_value = 0
        for key, value in self.books.items():
            if(value > most_read_value):
                most_read_key = key
                most_read_value = value
        return most_read_key

    def highest_rated_book(self):
        highest_rated_book = ""
        book_rating = 0
        book_average_rating = 0
        for book in self.books:
            book_average_rating = book.get_average_rating()
            if(book_average_rating > book_rating):
                highest_rated_book = book.get_title()
                book_rating = book_average_rating
        return highest_rated_book

    def most_positive_user(self):
        ## get the User object and use get_average_rating to find best rating
        most_positive_user = ""
        book_rating = 0
        book_average_rating = 0
        for user in self.users.values():
            book_average_rating = user.get_average_rating()
            if(book_average_rating > book_rating):
                most_positive_user = user.name
                book_rating = book_average_rating
        return most_positive_user

    def __repr__(self):
        TomeRater_str = ""
        print(TomeRater) ## print type
        ## show users
        for key, value in self.users.items():
            print(value)
        return TomeRater_str

    def __eq__(self, other_TomeRater):
        if((self.users == other_TomeRater.users) and (self.books == other_TomeRater.books)):
            return True
        else:
            return False

    ## return list of N most read books in descending order
    def get_n_most_read_books(self, n):
        copy_user_books = {}
        sorted_user_books = {}

        ## create a copy of the self.books dict.
        copy_user_books = self.books.copy()

        ## if n exceeds total number of books, then set n to total number of books
        if(n > len(self.books)):
            n = len(self.books)

        ## loop through n times
        for i in range(0, n):
            most_read = 0
            most_read_key = 0

            ## sort out the most read book and its key and save  them
            for key, value in copy_user_books.items():
                if(value > most_read):
                    most_read = value
                    most_read_key = key

            ## then remove it from the copy list. do this n times.
            sorted_user_books[most_read_key] = most_read ## create new dictionary entry
            copy_user_books.pop(most_read_key) ## remove from dictionary

        return sorted_user_books


    ## return list of N most prolific readers in descending order
    def get_n_most_prolific_readers(self, n):
        copy_users = {}
        sorted_users = {}

        ## create a copy of the self.users dict.
        copy_users = self.users.copy()

        ## if n exceeds total number of users, then set n to total number of users
        if(n > len(self.users)):
            n = len(self.users)

        ## loop through n times
        for i in range(0, n):
            most_read = 0
            most_read_key = 0
            most_read_user = 0

            ## sort out the which user read the most books
            for key, user in copy_users.items():
                ## object contains the User object
                number_of_books = user.number_books_read()
                if(number_of_books > most_read):
                    most_read = number_of_books
                    most_read_key = key
                    most_read_user = user

            ## then remove it from the copy list. do this n times.
            sorted_users[most_read_key] = most_read_user ## create new dictionary entry
            copy_users.pop(most_read_key) ## remove from dictionary

        return sorted_users

    # return list of N most expensive books
    def get_n_most_expensive_books(self, n):
        pass

    # return total of $ spent on books read
    def get_worth_of_user(self, user_email):
        pass


## User class - allows creation and maintenance of User object.
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {} ## book object -> ratings

    ## return email for user
    def get_email(self):
        return self.email

    ## change email for user
    def change_email(self, address):
        print("email address changed from", self.email, "to", address)
        self.email = address


    def __repr__(self):
        user_string = []
        user_string = "User: " + self.name + ", " + "email: " + self.email + ", " "Books Read: " + str(len(self.books))
        return user_string

    def __eq__(self, other_user):
        if(self.name == other_user.name and self.email == other_user.email):
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0;
        count = 0
        average_rating = 0
        if(len(self.books) > 0):
            for value in self.books.values():
                if(value == None):
                    count += 1  ## None counts against average
                else:
                    total_rating += value
                    count += 1
            average_rating = total_rating / count
        else:
            average_rating = 0

        return average_rating

    ## length should indicate number of entriesin dictionary thus number
    ## of booksread
    def number_books_read(self):
        return len(self.books)

## class Book - allows creation and maintenance of book object.
class Book():

    def __init__(self, title, isbn, price = 0):
        ## make sure the ISBN has not been used
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        print("ISBN number changed from ", self.isbn, "to ", isbn)
        self.isbn = isbn

    def add_rating(self, rating):
        ## if rating in none then it is invalid
        if(rating == None):
            print("Invalid Rating")
        elif (rating >= 0 and rating <= 4): ## if the rating is valid then append to list
            self.ratings.append(rating) ## add valid rating
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if(other_book.title == self.title and other_book.isbn == self.isbn):
            return True
        else:
            return False
        pass

    def get_average_rating(self):
        total_rating = 0;
        count = 0
        average_rating = 0
        if(len(self.ratings) > 0): ## at least 1 rating
            for rating in self.ratings:
                total_rating += rating
                count += 1
            average_rating = total_rating / count

        return average_rating

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        book_str = []
        book_str = self.title
        return book_str

    def add_price(self, price):
        self.price = price



class Fiction(Book):

    def __init__(self, title, author, isbn, price = 0):
        super().__init__(title, isbn)
        self.author = author


    def get_author(self):
        return self.author

    def __repr__(self):
        book_str = []
        book_str = self.title + " by "  + self.author
        return book_str



class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn, price = 0):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level


    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        book_str = []
        book_str = self.title + ", a "  + self.level + " manual on " + self.subject
        return book_str


##================================================================
## The followibg lines are used to test the TomeRater application
## this has been moved from the populate.py file
##================================================================
Tome_Rater = TomeRater()

#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

novel4 = Tome_Rater.create_novel("Tome Rater", "Phil Jerzak", 11111938)


#Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

Tome_Rater.add_user("Phillip Jerzak", "phillip.jerzak@oracle.com")

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

# already entered as a user
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])
# invalid email
Tome_Rater.add_user("Phil Jerzak", "phil.jerzaknc.rr.com")
# invalid email
Tome_Rater.add_user("Phil Jerzak", "phil.jerzak@nc.rr.gov")


#Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

## add book with different title but a duplicate ISBN
Tome_Rater.add_book_to_user(novel4, "phillip.jerzak@oracle.com", 4)


#Uncomment these to test your functions:
Tome_Rater.print_catalog()
Tome_Rater.print_users()

print("Most positive user:")
print(Tome_Rater.most_positive_user())
print("\n\r")

print("Highest rated book:")
print(Tome_Rater.highest_rated_book())
print("\n\r")

print("Most read book:")
print(Tome_Rater.most_read_book())

## print object
print("\n\r\n\r\n\r")
print(Tome_Rater)

## create new
Tome_Rater2 = TomeRater()

if(Tome_Rater == Tome_Rater2):
    print("\n\rOjects are equal\n\r")
else:
    print("\n\rOjects are not equal\n\r")

## copy original
Tome_Rater2 = Tome_Rater

if(Tome_Rater == Tome_Rater2):
    print("\n\rOjects are equal\n\r")
else:
    print("\n\rOjects are not equal\n\r")

## most read book
print("======= Most Read Books =======\n\r")
print(Tome_Rater.get_n_most_read_books(5))

print("\n\r)")

## users that have read the most books
print("======= Users with most read books =======\n\r")
print(Tome_Rater.get_n_most_prolific_readers(3))


print("\n\rend of program\n\r")

