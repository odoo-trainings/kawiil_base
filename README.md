# kawiil_base

> [!WARNING]
> **Training use only. Do not install any of the modules in this repository (`kawiil_base`, `kawiil_website`) on a
> production database or on a database linked to an active Odoo subscription.** They rename the company and the
> administrator, change the company logo, address and currency, create users with published passwords, and load
> fictional customers, vendors, employees and sale orders. Install them only on a new, disposable training database.

This module sets up the Technical Training Production Database using data files. Serves as the 3PA Module install task.

It loads the base data of K'awiil Motors, a fictional US maker of electric motorcycles with in-house financing
(Odoo 20.0). All people, companies, addresses, emails and phone numbers in it are fictional.

## What it creates

- **Company**: the main company becomes K'awiil Motors (San Francisco, California, USD), with the K'awiil logo.
- **Administrator**: the admin user is renamed Itzel Admin, CEO.
- **Users**: a sales manager, a sales representative and a finance user (see below).
- **Employees**: 5 departments (Management, Sales, Assembly, After-sales Service, Finance), 10 job positions and
  12 employees, with Itzel Admin at the top of the hierarchy. The admin and the three training users are employees.
- **Products**:
  - three bikes with 6 variants each (Battery x Color): K'awiil Raijin (sport), K'awiil Ukko (adventure) and
    K'awiil Indra (urban commuter). All three come in Jade Arc, Night Strike and Storm White. The extended
    battery adds a price extra; variant references look like `KWL-RAI-20-NST`. Each colour has its own product image;
  - K'awiil Xolotl, an off-road bike still in development: not for sale (`kawiil_website` keeps it off the shop);
  - 10 bought-in goods (chargers, cable, rider gear, parts) and 2 services (extended warranty, annual service).
- **Vendors**: 6 US suppliers with vendor prices, minimum quantities and lead times on the bought-in goods.
  The bikes are made in-house and have no vendor.
- **Customers**: 8 individuals and 2 companies across the US.
- **Sales**: 30 sale orders split between the two salespeople: 20 confirmed orders, 5 quotations, 3 sent
  quotations and 2 cancelled ones. Quotations are dated in the past; confirmed orders are dated on the install day.
  The confirmed orders are an open backlog: nothing is delivered or invoiced yet, so trainees can process them.
- **Settings**: Variants is enabled (through `res.config.settings`, as if saved from the Settings screen).
- **Employee photos**: Itzel, Tomás, Diego and Arjun have portrait photos (also used on the website About page).
- **Taxes**: none. Products and orders carry no taxes, and no US localization is installed.

All data files are `noupdate`: updating the module does not overwrite what trainees changed.

## Training users

| Login | Password | Name | Access |
| --- | --- | --- | --- |
| `sales.manager` | `kawiil-manager` | Diego Ramírez | Sales: Administrator |
| `sales.rep` | `kawiil-rep` | Hannah Lee | Sales: User, own documents only |
| `finance` | `kawiil-finance` | Arjun Mehta | Invoicing: Administrator |

The admin login and password are not changed by this module.

## kawiil_website

The K'awiil Motors website, built from the design handoff in `design_handoff_kawiil_odoo20/` (`HANDBACK.md` is
the source of truth). It depends on `kawiil_base`, `website_sale` and `website_crm`.

- **Theme**: K'awiil palette (Jade, Mint Arc, Mist, white, Night), Barlow and Barlow Condensed from Google Fonts,
  square buttons, dark header and footer, the K'awiil logo and favicon. Values changed later in the website builder
  still take precedence. The website configurator is marked as done so it does not replace the theme.
- **Pages**: home, `/raijin`, `/ukko`, `/indra`, `/financing`, `/financing/apply`, `/about` and `/test-ride`, each
  built from standard website building blocks so they stay editable in the builder.
- **Menu**: Models (Raijin, Ukko, Indra), Financing, Shop, About, and a "Book a test ride" button.
- **Forms**: the test ride form and the financing enquiry form create CRM leads for the Sales team.
  `/financing/apply` is a placeholder until the loan application module exists.
- **Settings**: CRM Leads is enabled (through `res.config.settings`), the Sales team uses leads, and it is the
  website's default team for form leads.
- **Shop**: publishes the bikes, gear, parts and services from `kawiil_base`. Xolotl stays unpublished.

Only compressed images are committed. The original design images stay in the ignored `images/` and
`design_handoff_kawiil_odoo20/uploads/` folders.

## Tests

Both modules ship post-install tests. Run them on a new database without demo data:

    odoo-bin --config=<your config> -i kawiil_base,kawiil_website --test-tags /kawiil_base,/kawiil_website
