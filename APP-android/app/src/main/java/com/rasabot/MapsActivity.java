package com.rasabot;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentActivity;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.Circle;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;
import com.rasabot.R;
import com.rasabot.databinding.ActivityMapsBinding;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback, GoogleMap.OnMapLongClickListener {
    static final Marker STATE_MARKER =null;
    static final GoogleMap STATE_MAP =null;
    private static final String STATE_KEY_MAP_CAMERA = null;
    private GoogleMap mMap;
    private ActivityMapsBinding binding;
    private Button button;
    private Circle circle;
    private Marker marker;

    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        // Save the user's current game state
        if (mMap != null) {
            savedInstanceState.putParcelable(STATE_KEY_MAP_CAMERA, mMap.getCameraPosition());
        }
        // Always call the superclass so it can save the view hierarchy state
        super.onSaveInstanceState(savedInstanceState);
    }


    // Register the permissions callback, which handles the user's response to the
    // system permissions dialog. Save the return value, an instance of
    // ActivityResultLauncher, as an instance variable.
    private ActivityResultLauncher<String> requestPermissionLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestPermission(), isGranted -> {
                if (isGranted) {
                    // Permission is granted. Continue the action or workflow in your
                    // app.
                    Log.d("here","here");
                    getLocation();
                } else {
                    // Explain to the user that the feature is unavailable because the
                    // features requires a permission that the user has denied. At the
                    // same time, respect the user's decision. Don't link to system
                    // settings in an effort to convince the user to change their
                    // decision.
                    Log.d("here","No permission");
                }
            });


    private FusedLocationProviderClient fusedLocationClient;
    private Location locationNow;
    private LocationCallback locationCallback;

    private LocationRequest locationRequest;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (savedInstanceState != null) {
            CameraUpdate cameraPos = CameraUpdateFactory.newCameraPosition(
                    (CameraPosition)(savedInstanceState.getParcelable(STATE_KEY_MAP_CAMERA)));
            mMap.moveCamera(cameraPos);
        }
        binding = ActivityMapsBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        setupMapIfNeeded();


        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);


        // fusedLocationClient
        fusedLocationClient= LocationServices.getFusedLocationProviderClient(this);


        fusedLocationClient.getLastLocation().addOnSuccessListener(this, new OnSuccessListener<Location>() {
            @Override
            public void onSuccess(Location location) {
                // Got last known location. In some rare situations this can be null.
                if (location != null) {
                    // Logic to handle location object
                    createLocationRequest();
                    Log.d("here","Create location: "+location.toString() + "locationRequest"+locationRequest.toString());
                }
            }
        });



        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {
                if (locationResult == null) {
                    return;
                }
                for (Location location : locationResult.getLocations()) {
                    // Update UI with location data
                    // ...
                    locationNow = location;
                    Log.d("here","Update location: "+location.toString());
                    LatLng latLng = new LatLng(locationNow.getLatitude(), locationNow.getLongitude());
                    MarkerOptions markerOptions =new MarkerOptions().position(latLng).title("Location");
                    marker.remove();
                    marker=mMap.addMarker(markerOptions);

                    mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng) );
                    mMap.moveCamera(CameraUpdateFactory.zoomTo(21));
                    break;
                }
                fusedLocationClient.removeLocationUpdates(this);
            }
        };




    }
    @Override
    protected void onPause() {
        super.onPause();
        MapStateManager mgr = new MapStateManager(this);
        mgr.saveMapState(mMap);
        Toast.makeText(this, "Map State has been save?", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        setupMapIfNeeded();
    }
    private void setupMapIfNeeded() {
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        if (mMap == null) {
            SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                    .findFragmentById(R.id.map);
            mapFragment.getMapAsync(this);
        }
    }
    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        //LatLng sydney = new LatLng(-34, 151);
        //marker=mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
        //mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
        try{
            Intent i = getIntent();
            float latitude = i.getFloatExtra("latitude", 0);
            float longitude = i.getFloatExtra("longitude", 0);
            markLocation(new LatLng(latitude, longitude));
            Log.d("map", "marking " + latitude + "," + longitude);
        } catch (Exception e) {
            e.printStackTrace();
        }
        //mMap.setOnMapLongClickListener(this);
        MapStateManager mgr = new MapStateManager(this);
        CameraPosition position = mgr.getSavedCameraPosition();
        if (position != null) {
            CameraUpdate update = CameraUpdateFactory.newCameraPosition(position);
            Toast.makeText(this, "entering Resume State", Toast.LENGTH_SHORT).show();
            mMap.moveCamera(update);

            mMap.setMapType(mgr.getSavedMapType());
        }

    }




    public void markLocation(LatLng location){

        marker=mMap.addMarker(new MarkerOptions().position(location).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(location));
    }



    public void onLocationButtonClicked(View view){



        if (ContextCompat.checkSelfPermission(
                getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) ==
                PackageManager.PERMISSION_GRANTED) {
            // You can use the API that requires the permission.

            getLocation();



        }
        else {
            // You can directly ask for the permission.
            // The registered ActivityResultCallback gets the result of this request.
            requestPermissionLauncher.launch(
                    Manifest.permission.ACCESS_FINE_LOCATION);

        }
    }




    private void getLocation(){

            fusedLocationClient.requestLocationUpdates(locationRequest,locationCallback, Looper.getMainLooper());


    }






    protected void createLocationRequest() {
        locationRequest = LocationRequest.create();
        locationRequest.setInterval(10000);
        locationRequest.setFastestInterval(5000);
        locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
    }


    @Override
    public void onMapLongClick(@NonNull LatLng latLng) {

    }
}