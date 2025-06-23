# Use the official Nginx image from Docker Hub
FROM nginx:1.25-alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration file from the host to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 (which is what Nginx will listen on by default as per our config)
EXPOSE 80

# Command to start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
