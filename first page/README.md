# LCA Dataset Page - Setup Guide

## Overview
This page allows users to select their data source for Life Cycle Assessment (LCA):
1. **Upload custom dataset** - Upload your own CSV/Excel/JSON files
2. **Use default datasets** - Choose from multiple sources:
   - OpenLCA Database (via API)
   - Ecoinvent Database
   - Indian LCA Database
   - Built-in Database

## OpenLCA API Integration

### Prerequisites
1. **Install OpenLCA**
   - Download from: https://www.openlca.org/download/
   - Install the application on your system

### Enabling OpenLCA REST API

1. **Start OpenLCA Application**
   - Launch the OpenLCA desktop application

2. **Enable IPC Server**
   - Go to: `Window` → `Developer Tools` → `IPC Server`
   - Click the **Start** button
   - The server will start on `http://localhost:8080`
   - Keep OpenLCA running in the background while using the web app

3. **Verify Connection**
   ```bash
   # Run the test script
   cd "d:\Lca project- new"
   py test_openlca_api.py
   ```

4. **Expected Output**
   ```
   ✅ Successfully connected to OpenLCA API!
   Found X database(s):
     - database_name_1
     - database_name_2
   ```

### Available OpenLCA Databases

Once OpenLCA is running, you can access:
- **Ecoinvent** (if imported)
- **ELCD** (European Reference Life Cycle Database)
- **US LCI** (US Life Cycle Inventory)
- **agribalyse** (French agricultural database)
- **Custom databases** you've created in OpenLCA

### API Endpoints Used

```python
# Check available databases
GET http://localhost:8080/databases

# Get processes (requires POST with JSON body)
POST http://localhost:8080/data/get/descriptors
Body: {"@type": "Process"}

# Get flows
POST http://localhost:8080/data/get/descriptors
Body: {"@type": "Flow"}

# Get impact methods
POST http://localhost:8080/data/get/descriptors
Body: {"@type": "ImpactMethod"}
```

## Alternative Data Sources

### 1. Indian LCA Database
- **Source**: Indian Life Cycle Database (ILCD)
- **Coverage**: Indian-specific data for energy, materials, transport
- **Access**: Regional data with 85-95% coverage

### 2. Ecoinvent Database
- **Source**: Global LCA database
- **Coverage**: 19,000+ processes worldwide
- **Note**: Requires commercial license
- **Website**: https://ecoinvent.org/

### 3. Built-in Database
- **Source**: MetaLCA default database
- **Coverage**: 1,200+ materials and processes
- **Data**: Global averages and industry standards

## File Structure

```
first page/
├── dataset.html              # Main HTML page
├── static/
│   ├── css/
│   │   └── dataset.css      # Styling
│   └── js/
│       └── dataset.js       # Frontend logic
└── dataset_routes.py        # Flask backend routes
```

## Integration with Main App

Add to your main `app.py`:

```python
from first_page.dataset_routes import dataset_bp

# Register blueprint
app.register_blueprint(dataset_bp)

# Update dashboard route to redirect to dataset page
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return redirect('/dataset')
```

## Usage Flow

1. **User logs in** → Redirected to Dataset Selection Page
2. **Choose data source**:
   - Option A: Upload custom files (CSV, Excel, JSON)
   - Option B: Select from default sources (OpenLCA, Ecoinvent, Indian, Built-in)
3. **System validates** data source availability
4. **User proceeds** to Input Data page with selected dataset

## Troubleshooting

### OpenLCA Connection Failed
```
❌ Connection failed!
```
**Solution**:
1. Ensure OpenLCA is running
2. Go to `Window` → `Developer Tools` → `IPC Server`
3. Click `Start`
4. Verify port 8080 is not blocked by firewall

### No Databases Found
```
OpenLCA connected but no active database
```
**Solution**:
1. Import a database in OpenLCA
2. Go to `File` → `Import` → `Linked Data (JSON-LD)`
3. Download databases from: https://nexus.openlca.org/databases

### Port Already in Use
```
Error: Port 8080 is already in use
```
**Solution**:
- Stop other services using port 8080
- Or change OpenLCA IPC Server port in settings

## Testing

Run the OpenLCA connectivity test:
```bash
cd "d:\Lca project- new"
py test_openlca_api.py
```

## Next Steps

After dataset selection, user proceeds to:
- **Input Data Page** - Enter product/process information
- **Confirm Data** - Review and validate inputs
- **Dashboard** - View LCA results and analysis

## References

- OpenLCA API Documentation: https://greendelta.github.io/olca-schema/
- OpenLCA Forum: https://ask.openlca.org/
- Indian LCA: http://www.teriin.org/
- Ecoinvent: https://ecoinvent.org/
