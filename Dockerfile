FROM node:16.19
WORKDIR .
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
COPY . .
CMD ["node", "source/index.js"]
