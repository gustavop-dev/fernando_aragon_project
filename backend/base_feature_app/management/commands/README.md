# Fake Data Management Commands

This directory contains Django commands to create and delete test data (fake data) in the database.

## 📋 Available Commands

### 1. Create Users

```bash
python manage.py create_users [number_of_users]
```

**Example:**
```bash
python manage.py create_users 15
```

**Note:** Users are created with the default password: `password123`

---

### 2. Create All Fake Data (Master Command)

```bash
python manage.py create_fake_data [number_of_records]
```

**Example with single number:**
```bash
python manage.py create_fake_data 20
```

**Example with specific user count:**
```bash
python manage.py create_fake_data --users 10
```

> **Note:** This master command also accepts `--blogs`, `--products`, and `--sales` flags inherited from the base template. These sub-commands (`create_blogs`, `create_products`, `create_sales`) are not present in the current project and will fail if invoked. Use `create_users` directly or pass `--users` only.

---

### 3. Delete All Fake Data

```bash
python manage.py delete_fake_data --confirm
```

**⚠️ IMPORTANT:**
- This command requires the `--confirm` flag to prevent accidental deletions.
- **WILL NOT delete** administrator users or superusers (automatic protection).

> **Note:** This command imports `Blog`, `Product`, and `Sale` models from the base template. If those models have been removed, the command will need to be updated to only delete Users.

---

## 🔒 Administrator User Protection

The `delete_fake_data` command is designed to **automatically protect** administrator users:

- ✅ **Keeps** users with `is_superuser=True`
- ✅ **Keeps** users with `is_staff=True`
- ❌ **Deletes** regular users (customers)

This ensures that system administration accounts are never accidentally deleted.

---

## 📊 Generated Data Structure

### User (`create_users`)
- Unique email
- First and last name
- Phone number
- Role: Customer or Admin (random)
- Default password: `password123`
- Admin users get `is_staff=True`

---

## 🎯 Recommended Workflow

1. **Create test users:**
   ```bash
   python manage.py create_users 10
   ```

2. **Work with the application** using the test data.

3. **Clean the database when finished:**
   ```bash
   python manage.py delete_fake_data --confirm
   ```

4. **Recreate data if needed.**

---

## 💡 Tips

- Fake users have the password `password123` for easy testing.
- Check the Django admin panel at `/admin` to manage users.
