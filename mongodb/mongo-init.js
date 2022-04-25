print("Creating application user...");
db = db.getSiblingDB("dims");
db.createUser({
  user: "dims_user",
  pwd: "dims_password",
  roles: [{ role: "readWrite", db: "dims" }],
});
print("Application user created");
