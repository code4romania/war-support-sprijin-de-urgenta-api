# Resource Volunteer Management Django API

[![GitHub contributors][ico-contributors]][link-contributors]
[![GitHub last commit][ico-last-commit]][link-last-commit]
[![License: MPL 2.0][ico-license]][link-license]

Insert bullets description of the project if available.

[See the project live][link-production]

Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project.

[Contributing](#contributing) | [Built with](#built-with) | [Related repositories](#related-repositories) | [Deployment](#deployment) | [Feedback](#feedback) | [License](#license) | [About Code for Romania](#about-code-for-romania)

## Contributing

This project is built by amazing volunteers and you can be one of them! Here's a list of ways in [which you can contribute to this project][link-contributing]. If you want to make any change to this repository, please **make a fork first**.

Help us out by testing this project in the [staging environment][link-staging]. If you see something that doesn't quite work the way you expect it to, open an Issue. Make sure to describe what you _expect to happen_ and _what is actually happening_ in detail.

If you would like to suggest new functionality, open an Issue and mark it as a __[Feature request]__. Please be specific about why you think this functionality will be of use. If you can, please include some visual description of what you would like the UI to look like, if you are suggesting new UI elements.

## Built With

### Programming languages

Python 3.9

### Backend framework

Django 3.2

### Package managers

pip

### Database technology & provider

PostgreSQL

## Related repositories

- **the client side of the app:**
  https://github.com/code4romania/war-support-sprijin-de-urgenta-client
- **the map of the resource collection centers:**
  https://github.com/code4romania/war-harta-sprijin-de-urgenta

## Deployment

Guide users through getting your code up and running on their own system. In this section you can talk about:
1. Make a copy of the `.env` file, change the variables and run the build command

    ```shell
    cp .env.dev .env
    # modify the variables in the .env and then build the development container
    make build-dev
    ```

2. Software dependencies

    You can run the app through docker, if it is installed on your machine. If you wish to run it manually you will need to have `gettext` installed.

### Environment variables

The `.env` files contain variables required to start the services and initialize them.

- `ENVIRONMENT` - [`test`|`development`|`production`] sets the type of deployment (default `production`)
- `RUN_MIGRATION` - [`True`|`False`] run django migrations when you start the app (default `True`)
- `RUN_COMPILEMESSAGES` - [`True`|`False`] compile i18n messages when you first start the app (default `True`)
- `RUN_SEED_DATA` - [`True`|`False`] load the data from the `fixtures/` folders (default `False`)
- `RUN_COLLECT_STATIC` - [`True`|`False`] collects static data like images/fonts (default `True` - has no effect if `ENVIRONMENT != production`)
- `RUN_DEV_SERVER` - [`True`|`False`] starts the app in development mode with a more comprehensive debugging toolbox (default `False`)
- `SECRET_KEY` - the secret key Django will use to encrypt data (should be changed if you're not running through Docker)

## Staging environment setup

When deploying onto a machine, there is no need to clone the whole project. You only need a `.env` and the `docker-compose.staging.yaml` file. This uses a [watchtower](https://github.com/containrrr/watchtower) contianer to watch for a new version of the `staging` tag of the `code4romania/sprijin-de-urgenta-api` docker image and update the containers as necessary.

## Feedback

* Request a new feature on GitHub.
* Vote for popular feature requests.
* File a bug in GitHub Issues.
* Email us with other feedback contact@code4.ro

## License

This project is licensed under the MPL 2.0 License - see the [LICENSE](LICENSE) file for details

## About Code for Romania

Started in 2016, Code for Romania is a civic tech NGO, official member of the Code for All network. We have a community of around 2.000 volunteers (developers, ux/ui, communications, data scientists, graphic designers, devops, it security and more) who work pro-bono for developing digital solutions to solve social problems. #techforsocialgood. If you want to learn more details about our projects [visit our site][link-code4] or if you want to talk to one of our staff members, please e-mail us at contact@code4.ro.

Last, but not least, we rely on donations to ensure the infrastructure, logistics and management of our community that is widely spread across 11 timezones, coding for social change to make Romania and the world a better place. If you want to support us, [you can do it here][link-donate].


[ico-contributors]: https://img.shields.io/github/contributors/code4romania/rvm-api-django.svg?style=for-the-badge
[ico-last-commit]: https://img.shields.io/github/last-commit/code4romania/rvm-api-django.svg?style=for-the-badge
[ico-license]: https://img.shields.io/badge/license-MPL%202.0-brightgreen.svg?style=for-the-badge

[link-contributors]: https://github.com/code4romania/rvm-api-django/graphs/contributors
[link-last-commit]: https://github.com/code4romania/rvm-api-django/commits/main
[link-license]: https://opensource.org/licenses/MPL-2.0
[link-contributing]: https://github.com/code4romania/.github/blob/main/CONTRIBUTING.md

[link-production]: https://api.sprijindeurgenta.ro
[link-staging]: https://sprijin-de-urgenta-api.heroesof.tech/

[link-code4]: https://www.code4.ro/en/
[link-donate]: https://code4.ro/en/donate/
