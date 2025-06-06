# Use an official Node runtime as a parent image
FROM node:18-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) first
# to leverage Docker cache for dependencies
COPY package*.json ./
# If using yarn, uncomment the next line and comment out the npm ci line
# COPY yarn.lock ./

# Install dependencies
# Use ci for cleaner installs in CI/CD environments
RUN npm ci
# If using yarn, uncomment the next line and comment out the npm ci line
# RUN yarn install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# --- Serve Stage ---
# Use a lightweight web server to serve the static files
FROM nginx:stable-alpine

# Copy the built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config file if you have custom configurations
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for nginx
EXPOSE 80

# Start nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]

