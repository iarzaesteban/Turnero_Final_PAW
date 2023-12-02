FROM php:7.4-apache

RUN apt-get update \
    && apt-get install -y git zip unzip libzip-dev libpq-dev \
    && docker-php-ext-install pdo pdo_pgsql zip

WORKDIR /var/www/html

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY composer.json .

COPY composer.lock .

RUN composer install --no-scripts --no-autoloader

COPY . .

RUN composer dump-autoload --optimize

EXPOSE 80
