# paperclip

Simple CRUD flask based app for accounting management system

## Getting started

This app is based on python, flask, sql tech-stack.

### Run app

To start app print in terminal

```
$ flask run
```

### Prerequisities

After downloading project make sure to install all requirements:

```
$ pip install -r requirements.txt
```

### Installing

To create a database main table

```
$ flask create_tables
```

To create additional database tables:

```
$ flask create_currencies
$ flask create_payments
$ flask create_categories
```

To create a sample data

```
$ flask create_invoices
```


### Testing queries

There is an option to test all the queries

```
$ flask test_query
```

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - the lightweight WSGI web application framework
* [Bootstrap](https://getbootstrap.com/) - the toolkit for developing with HTML, CSS, and JS
* [SQLAlchemy](https://www.sqlalchemy.org/) - the database toolkit for python

## Author

* **Radoslaw Sobieralski** - *Initial work* - [github](https://github.com/radoslawsobieralski)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
