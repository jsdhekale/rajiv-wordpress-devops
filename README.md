# Rajiv WordPress DevOps (MVP)

This repo contains the MVP Dockerfile used to build a custom WordPress image and push it to AWS ECR (Mumbai).

## Image
- Base: wordpress:6.9.1-php8.2-apache
- Custom tag: rajiv-wordpress:dev
- ECR: 969318514380.dkr.ecr.ap-south-1.amazonaws.com/rajiv-wordpress:dev

## Build (local)
docker build -t rajiv-wordpress:dev .

## Tag + Push (ECR)
docker tag rajiv-wordpress:dev 969318514380.dkr.ecr.ap-south-1.amazonaws.com/rajiv-wordpress:dev
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 969318514380.dkr.ecr.ap-south-1.amazonaws.com
docker push 969318514380.dkr.ecr.ap-south-1.amazonaws.com/rajiv-wordpress:dev
