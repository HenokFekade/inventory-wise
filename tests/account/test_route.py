import pytest

from apps.account.schemas.account import CreateAccountModelSchema
from utils.enums.account_role import AccountRole
from utils.password import PasswordHelper


@pytest.fixture
def super_admin_account(test_account_repo, test_client):
    account = test_account_repo.store(CreateAccountModelSchema(
        first_name=f"Super",
        last_name="admin",
        email=f"super.admin@example.com",
        phone=f"+251934567891",
        role=AccountRole.super_admin,
        password=PasswordHelper.hash("password"),
        is_active=True,
        password_change_required=False,
    ))

    response = test_client.post(
        "/api/v1/auth/login/account",
        json={"email": account.email, "password": "password"},
    )

    assert response.status_code == 200
    return response.json()["token"]["access_token"]


@pytest.fixture
def admin_account(test_account_repo, test_client):
    account = test_account_repo.store(CreateAccountModelSchema(
        first_name=f"Admin",
        last_name="User",
        email=f"admin@example.com",
        phone=f"+251934567892",
        role=AccountRole.admin,
        password=PasswordHelper.hash("password"),
        is_active=True,
        password_change_required=False,
    ))
    return account


@pytest.fixture
def admin_account_token(test_account_repo, test_client):
    account = test_account_repo.store(CreateAccountModelSchema(
        first_name=f"Admin",
        last_name="User",
        email=f"admin@example.com",
        phone=f"+251934567892",
        role=AccountRole.admin,
        password=PasswordHelper.hash("password"),
        is_active=True,
        password_change_required=False,
    ))

    response = test_client.post(
        "/api/v1/auth/admin/login",
        json={"email": account.email, "password": "password"},
    )

    assert response.status_code == 200
    return response.json()["token"]["access_token"]


@pytest.fixture
def sample_5_accounts(test_account_repo):
    """Creates 5 test accounts in the database"""
    accounts = []
    for i in range(5):
        account = test_account_repo.store(CreateAccountModelSchema(
            first_name=f"User{i}",
            last_name="Test",
            email=f"user{i}@example.com",
            phone=f"+25193456788{i}",
            role=AccountRole.admin,
            password="hashed_password",
            is_active=True,
            password_change_required=False,
        ))
        accounts.append(account)
    return accounts


@pytest.mark.asyncio
async def test_list_accounts_unauthenticated(test_client):
    response = test_client.get("/api/v1/accounts")
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"

# def test_list_accounts_unauthorized(test_client, admin_account_token):
#     _id = str(uuid.uuid4())
#     token = admin_account_token
#     response = test_client.get("/api/v1/accounts", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 403
#     print(response.json())
#     assert response.json()["message"] == "You are not authorized to perform this action"
#     response = test_client.post("/api/v1/accounts", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 403
#     assert response.json()["message"] == "You are not authorized to perform this action"
#     response = test_client.get(f"/api/v1/accounts/{_id}", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 403
#     assert response.json()["message"] == "You are not authorized to perform this action"
#     response = test_client.patch(f"/api/v1/accounts/{_id}", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 403
#     assert response.json()["message"] == "You are not authorized to perform this action"
#     # TODO: add user role
#
# def test_empty_accounts_success(test_client, super_admin_account):
#     token = super_admin_account
#     response = test_client.get("/api/v1/accounts", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Accounts fetched successfully"
#     assert response.json()["total"] == 0
#     assert response.json()["page"] == 1
#     assert response.json()["per_page"] == 10
#
# def test_list_accounts_success(test_client, super_admin_account, sample_5_accounts):
#     response = test_client.get("/api/v1/accounts", headers=get_authorization_header(super_admin_account))
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data["data"]) == len(sample_5_accounts)
#     assert data["total"] == len(sample_5_accounts)
#     assert data["page"] == 1
#     assert data["per_page"] == 10
#
# def test_create_account_duplicate_email(test_client, test_db, super_admin_account, admin_account):
#     payload = {
#         "first_name": admin_account.first_name,
#         "last_name": admin_account.last_name,
#         "email": admin_account.email,
#         "phone": admin_account.phone,
#         "role": admin_account.role.name,
#         "password": "password",
#         "image": "https://image.com/png/profile.png",
#     }
#
#     response = test_client.post("/api/v1/accounts", json=payload, headers=get_authorization_header(super_admin_account))
#     data = response.json()
#     assert response.status_code == 422
#     assert "validation error" == data["message"]
#     assert "email" == response.json()["errors"][0]["name"]
#     assert "Email already taken" == response.json()["errors"][0]["messages"][0]
#
# def test_create_account_duplicate_phone(test_client, test_db, super_admin_account, admin_account):
#     payload = {
#         "first_name": admin_account.first_name,
#         "last_name": admin_account.last_name,
#         "email": "test@example.com",
#         "phone": admin_account.phone,
#         "role": admin_account.role.name,
#         "password": "password",
#         "image": "https://image.com/png/profile.png",
#     }
#
#     response = test_client.post("/api/v1/accounts", json=payload, headers=get_authorization_header(super_admin_account))
#
#     data = response.json()
#     assert response.status_code == 422
#     assert "validation error" == data["message"]
#     assert "phone" == response.json()["errors"][0]["name"]
#     assert "phone already taken" == response.json()["errors"][0]["messages"][0].lower()
#
# def test_create_account_invalid_input(test_client, super_admin_account):
#     response = test_client.post("/api/v1/accounts", json={}, headers=get_authorization_header(super_admin_account))
#
#     assert response.status_code == 422
#     errors = response.json()["detail"]
#     for error in errors:
#         assert error["loc"][-1] in ["first_name", "last_name", "email", "phone", "role", "password", "image"]
#         assert error["type"] == "missing"
#         assert error["msg"] == "Field required"
#
# def test_create_account_invalid_ethiopian_phone(test_client, super_admin_account):
#     invalid_phones = [
#         "+25191234567",    # Too short (9 digits)
#         "+2519123456789",  # Too long (11 digits)
#         "+261912345678",   # Wrong country code
#         "912345678",      # Missing +251
#         "+251012345678",   # Invalid starting digit (0)
#         "+25191234567a"    # Contains letter
#     ]
#
#     for phone in invalid_phones:
#         payload = {
#             "first_name": "John", "last_name": "Doe",
#             "email": f"test{phone}@example.com",  # Unique email for each test
#             "phone": phone, "role": AccountRole.admin.name,
#             "password": "password",
#         }
#
#         response = test_client.post(
#             "/api/v1/accounts",
#             json=payload,
#             headers=get_authorization_header(super_admin_account)
#         )
#
#         assert response.status_code == 422
#         error = response.json()["detail"][0]
#         assert error["loc"][-1] == "phone"
#         assert error["type"] == "value_error"
#         assert error["msg"] == "Value error, Invalid ethiopian phone number"
#
# def test_create_account_success(test_client, super_admin_account, test_db):
#     payload = {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": "john.doe@example.com",
#         "phone": "+251912345677",
#         "role": AccountRole.admin.name,
#         "password": "password",
#         "image": "https://image.com/png/profile.png",
#     }
#     response = test_client.post("/api/v1/accounts", json=payload, headers=get_authorization_header(super_admin_account))
#
#     assert response.status_code == 201
#     data = response.json()
#
#     account_data = data["data"]
#     for field in ["first_name", "last_name", "email", "phone", "role"]:
#         assert account_data[field] == payload[field], f"Mismatch in {field}"
#
#     # check database
#     account = test_db.query(AccountModel).filter(AccountModel.id == uuid.UUID(account_data["id"])).first()
#     assert account is not None
#     for field in ["first_name", "last_name", "email", "phone", "role"]:
#         value = getattr(account, field) if field != "role" else getattr(account, field).name
#         assert value == payload[field], f"Mismatch in {field}"
#
# def test_find_account_by_id_success(test_client, super_admin_account, sample_5_accounts):
#     account = sample_5_accounts[0]
#     response = test_client.get(f"/api/v1/accounts/{account.id}", headers=get_authorization_header(super_admin_account))
#     assert response.status_code == 200
#     data = response.json()
#     account_data = data["data"]
#     account_payload = AccountSchema.model_validate(account).model_dump(mode="json")
#     for field in ["first_name", "last_name", "email", "phone", "role"]:
#         assert account_data[field] == account_payload[field], f"Mismatch in {field}"
#
# def test_find_account_by_id_not_found(test_client, super_admin_account):
#     response = test_client.get(f"/api/v1/accounts/{uuid.uuid4()}", headers=get_authorization_header(super_admin_account))
#     assert response.status_code == 404
#
# def test_update_account_success(test_client, test_db, super_admin_account, admin_account):
#     """Test successful account update"""
#     update_data = {
#         "first_name": "UpdatedFirstName",
#         "last_name": "UpdatedLastName",
#         "email": "updated.email@example.com",
#         "phone": "+251987654321",
#         "role": AccountRole.super_admin.name,
#         "is_active": False,
#         "password": "new_password",
#         "image": "https://image.com/png/update-profile.png",
#     }
#
#     response = test_client.patch(
#         f"/api/v1/accounts/{admin_account.id}",
#         json=update_data,
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     assert response.status_code == 200
#     response_data = response.json()
#
#     # Verify response
#     assert response_data["message"] == "Account updated successfully"
#     for field in ["first_name", "last_name", "email", "phone", "role"]:
#         assert response_data["data"][field] == update_data[field]
#
#     # Verify database
#     updated_account = test_db.query(AccountModel).filter_by(id=admin_account.id).first()
#     for field in ["first_name", "last_name", "email", "phone"]:
#         assert getattr(updated_account, field) == update_data[field]
#     assert updated_account.role.name == update_data["role"]
#
# @pytest.mark.asyncio
# async def test_update_account_duplicate_email(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
# ):
#     _id = str(sample_5_accounts[1].id)
#     """Test updating to an existing email"""
#     existing_email = sample_5_accounts[0].email
#     update_data = {
#         "email": existing_email,
#         "phone": "+251987654321"  # Changing phone to avoid phone conflict
#     }
#
#     response = test_client.patch(
#         f"/api/v1/accounts/{str(_id)}",
#         json=update_data,
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     data = response.json()
#     assert response.status_code == 422
#     assert "validation error" == data["message"]
#     assert "email" == response.json()["errors"][0]["name"]
#     assert "email already taken" == response.json()["errors"][0]["messages"][0].lower()
#
# async def test_update_account_duplicate_phone(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
# ):
#     _id = str(sample_5_accounts[1].id)
#     existing_phone = sample_5_accounts[0].phone
#     update_data = {
#         "phone": existing_phone,
#         "email": "unique.email@example.com"  # Changing email to avoid email conflict
#     }
#
#     response = test_client.patch(
#         f"/api/v1/accounts/{str(_id)}",
#         json=update_data,
#         headers=get_authorization_header(super_admin_account)
#     )
#     data = response.json()
#     assert response.status_code == 422
#     assert "validation error" == data["message"]
#     assert "phone" == response.json()["errors"][0]["name"]
#     assert "phone already taken" == response.json()["errors"][0]["messages"][0].lower()
#
#
# async def test_update_account_invalid_phone(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
# ):
#     _id = str(sample_5_accounts[1].id)
#     """Test updating with invalid Ethiopian phone format"""
#     invalid_phones = [
#         "+25191234567",  # Too short (9 digits)
#         "+2519123456789",  # Too long (11 digits)
#         "+261912345678",  # Wrong country code
#         "912345678",  # Missing +251
#         "+251012345678",  # Invalid starting digit (0)
#         "+25191234567a"  # Contains letter
#     ]
#
#     for phone in invalid_phones:
#         response = test_client.patch(
#             f"/api/v1/accounts/{str(_id)}",
#             json={"phone": phone},
#             headers=get_authorization_header(super_admin_account)
#         )
#
#         assert response.status_code == 422
#         error = response.json()["detail"][0]
#         assert error["loc"][-1] == "phone"
#         assert error["type"] == "value_error"
#         assert error["msg"] == "Value error, Invalid ethiopian phone number"
#
# def test_update_account_not_found(test_client, super_admin_account):
#     """Test updating non-existent account"""
#     non_existent_id = uuid.uuid4()
#     update_data = {
#         "first_name": "NewName"
#     }
#
#     response = test_client.patch(
#         f"/api/v1/accounts/{non_existent_id}",
#         json=update_data,
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     assert response.status_code == 404
#     assert "account not found" in response.json()["message"].lower()
#
# async def test_change_password_account_invalid_input(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
#         test_token_service,
# ):
#     response = test_client.put(
#         f"/api/v1/accounts/change-password",
#         json={},
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     assert response.status_code == 422
#     for error in response.json()["detail"]:
#         assert error["loc"][-1] in ["password", "new_password", "confirm_password"]
#         assert error["type"] == "missing"
#         assert error["msg"] == "Field required"
#
# async def test_change_password_account_success(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
#         test_token_service,
# ):
#     payload = {
#         "password": "password",
#         "new_password": "pass@34",
#         "confirm_password": "pass@34",
#     }
#     response = test_client.put(
#         f"/api/v1/accounts/change-password",
#         json=payload,
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     data = response.json()
#     assert response.status_code == 200
#     assert data["message"] == "Password changed successfully"
#     assert data["data"]["first_name"] is not None
#     assert data["data"]["last_name"] is not None
#     assert data["data"]["phone"] is not None
#     assert data["data"]["email"] is not None
#     assert data["data"]["is_active"] is not None
#
#
# async def test_profile_account_success(
#         test_client,
#         test_db,
#         super_admin_account,
#         admin_account_token,
#         sample_5_accounts,
#         test_token_service,
# ):
#     response = test_client.get(
#         f"/api/v1/accounts/profile",
#         headers=get_authorization_header(super_admin_account)
#     )
#
#     data = response.json()
#     assert response.status_code == 200
#     assert data["message"] == "Profile fetched successfully"
#     assert data["data"]["first_name"] is not None
#     assert data["data"]["last_name"] is not None
#     assert data["data"]["phone"] is not None
#     assert data["data"]["email"] is not None
#     assert data["data"]["is_active"] is not None
