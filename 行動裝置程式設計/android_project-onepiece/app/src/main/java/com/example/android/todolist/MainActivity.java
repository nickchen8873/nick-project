/*
* Copyright (C) 2016 The Android Open Source Project
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package com.example.android.todolist;

import android.Manifest;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.LoaderManager;
import android.support.v4.content.AsyncTaskLoader;
import android.support.v4.content.Loader;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.helper.ItemTouchHelper;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.example.android.todolist.data.TaskContract;

import java.text.DateFormat;
import java.util.Calendar;


public class MainActivity extends AppCompatActivity implements
        LoaderManager.LoaderCallbacks<Cursor>, CustomCursorAdapter.ListItemClickListener {


    // Constants for logging and referring to a unique loader
    static int index ;
    static String important;
    static boolean flag=false;
    private static final String TAG = MainActivity.class.getSimpleName();
    private static final int TASK_LOADER_ID = 0;
    private int i =1;

    // Member variables for the adapter and RecyclerView
    private CustomCursorAdapter mAdapter;
    RecyclerView mRecyclerView;
    static Switch musicOnSwitch;
    static MediaPlayer mp;
    private static final int MY_PERMISSION_RECORD_AUDIO_REQUEST_CODE=88;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setupPermissions();
        // Set the RecyclerView to its corresponding view
        mRecyclerView = (RecyclerView) findViewById(R.id.recyclerViewTasks);


        // Set the layout for the RecyclerView to be a linear layout, which measures and
        // positions items within a RecyclerView into a linear list
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));

        // Initialize the adapter and attach it to the RecyclerView
        mAdapter = new CustomCursorAdapter(this,this);
        mRecyclerView.setAdapter(mAdapter);
        FloatingActionButton fabQuiz = findViewById(R.id.fab_quiz);
        fabQuiz.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startQuiz();
            }
        });


        /*
         Add a touch helper to the RecyclerView to recognize when a user swipes to delete an item.
         An ItemTouchHelper enables touch behavior (like swipe and move) on each ViewHolder,
         and uses callbacks to signal when a user is performing these actions.
         */
        new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0, ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
            @Override
            public boolean onMove(RecyclerView recyclerView, RecyclerView.ViewHolder viewHolder, RecyclerView.ViewHolder target) {
                return false;
            }

            // Called when a user swipes left or right on a ViewHolder
            @Override
            public void onSwiped(RecyclerView.ViewHolder viewHolder, int swipeDir) {
                // Here is where you'll implement swipe to delete

                // COMPLETED (1) Construct the URI for the item to delete
                //[Hint] Use getTag (from the adapter code) to get the id of the swiped item
                // Retrieve the id of the task to delete
                int id = (int) viewHolder.itemView.getTag();

                // Build appropriate uri with String row id appended
                String stringId = Integer.toString(id);
                Uri uri = TaskContract.TaskEntry.CONTENT_URI;
                uri = uri.buildUpon().appendPath(stringId).build();

                // COMPLETED (2) Delete a single row of data using a ContentResolver
                getContentResolver().delete(uri, null, null);

                // COMPLETED (3) Restart the loader to re-query for all tasks after a deletion
                getSupportLoaderManager().restartLoader(TASK_LOADER_ID, null, MainActivity.this);

            }
        }).attachToRecyclerView(mRecyclerView);

        /*
         Set the Floating Action Button (FAB) to its corresponding View.
         Attach an OnClickListener to it, so that when it's clicked, a new intent will be created
         to launch the AddTaskActivity.
         */
        FloatingActionButton fabButton = (FloatingActionButton) findViewById(R.id.fab);

        fabButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Create a new intent to start an AddTaskActivity
                Intent addTaskIntent = new Intent(MainActivity.this, AddTaskActivity.class);
                startActivity(addTaskIntent);
            }
        });

        /*
         Ensure a loader is initialized and active. If the loader doesn't already exist, one is
         created, otherwise the last created loader is re-used.
         */
        getSupportLoaderManager().initLoader(TASK_LOADER_ID, null, this);
    }

    private void startQuiz() {
        Intent intent = new Intent(MainActivity.this, QuizActivity.class);
        startActivity(intent);
    }

    /**
     * This method is called after this activity has been paused or restarted.
     * Often, this is after new data has been inserted through an AddTaskActivity,
     * so this restarts the loader to re-query the underlying data for any changes.
     */
    @Override
    protected void onResume() {
        super.onResume();
        if (flag) {
            mp.pause();
            mp.start();
        }
        // re-queries for all tasks
        getSupportLoaderManager().restartLoader(TASK_LOADER_ID, null, this);
    }


    /**
     * Instantiates and returns a new AsyncTaskLoader with the given ID.
     * This loader will return task data as a Cursor or null if an error occurs.
     *
     * Implements the required callbacks to take care of loading data at all stages of loading.
     */
    @Override
    public Loader<Cursor> onCreateLoader(int id, final Bundle loaderArgs) {

        return new AsyncTaskLoader<Cursor>(this) {

            // Initialize a Cursor, this will hold all the task data
            Cursor mTaskData = null;

            // onStartLoading() is called when a loader first starts loading data
            @Override
            protected void onStartLoading() {
                if (mTaskData != null) {
                    // Delivers any previously loaded data immediately
                    deliverResult(mTaskData);
                } else {
                    // Force a new load
                    forceLoad();
                }
            }

            // loadInBackground() performs asynchronous loading of data
            @Override
            public Cursor loadInBackground() {
                // Will implement to load data

                // Query and load all task data in the background; sort by priority
                // [Hint] use a try/catch block to catch any errors in loading data
                //排序方式

                try {
                    if (i == 1) {
                        return getContentResolver().query(TaskContract.TaskEntry.CONTENT_URI,
                                null,
                                null,
                                null,
                                TaskContract.TaskEntry.COLUMN_PRIORITY);
                    } else if (i == 2){
                        return getContentResolver().query(TaskContract.TaskEntry.CONTENT_URI,
                                null,
                                null,
                                null,
                                TaskContract.TaskEntry.COLUMN_DESCRIPTION);
                    }else{
                        return getContentResolver().query(TaskContract.TaskEntry.CONTENT_URI,
                                null,
                                null,
                                null,
                                TaskContract.TaskEntry.COLUMN_PRIORITY);
                    }
                } catch (Exception e) {
                    Log.e(TAG, "Failed to asynchronously load data.");
                    e.printStackTrace();
                    return null;
                }
            }

            // deliverResult sends the result of the load, a Cursor, to the registered listener
            public void deliverResult(Cursor data) {
                mTaskData = data;
                super.deliverResult(data);
            }
        };

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // 設置要用哪個menu檔做為選單
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }

    public boolean onOptionsItemSelected(MenuItem item) {

        // 取得點選項目的id
        int id = item.getItemId();


        if (id == R.id.action_sort) {
            if(this.i==1) {
                changeSort(2);
            }else{
                changeSort(1);
            }


            // COMPLETED (3) Restart the loader to re-query for all tasks after a deletion
            getSupportLoaderManager().restartLoader(TASK_LOADER_ID, null, MainActivity.this);
            return true;
        }
        if (id == R.id.action_settings) {
            Intent startSettingsActivity = new Intent(this, SettingActivity.class);
            startActivity(startSettingsActivity);
            return true;
        }


        return super.onOptionsItemSelected(item);
    }

    public void changeSort(int i){
        this.i = i;
        getSupportLoaderManager().restartLoader(TASK_LOADER_ID, null, MainActivity.this);
    }


    /**
     * Called when a previously created loader has finished its load.
     *
     * @param loader The Loader that has finished.
     * @param data The data generated by the Loader.
     */
    @Override
    public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
        // Update the data that the adapter uses to create ViewHolders
        mAdapter.swapCursor(data);
    }


    /**
     * Called when a previously created loader is being reset, and thus
     * making its data unavailable.
     * onLoaderReset removes any references this activity had to the loader's data.
     *
     * @param loader The Loader that is being reset.
     */
    @Override
    public void onLoaderReset(Loader<Cursor> loader) {
        mAdapter.swapCursor(null);
        }

    @Override
    public void onListItemClick(String description, int clickedItemIndex) {
        index = clickedItemIndex;
        important = description;
        Intent intent = new Intent(MainActivity.this, ItemActivity.class);
        startActivity(intent);
    }
    private void setupPermissions() {
        // If we don't have the record audio permission...
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            // And if we're on SDK M or later...
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                // Ask again, nicely, for the permissions.
                String[] permissionsWeNeed = new String[]{ Manifest.permission.WRITE_EXTERNAL_STORAGE };

                requestPermissions(permissionsWeNeed, MY_PERMISSION_RECORD_AUDIO_REQUEST_CODE);
            }
        } else {
            // Otherwise, permissions were granted and we are ready to go!

            mp = MediaPlayer.create(this, R.raw.onepiece2);
            mp.setLooping(true);
            mp.start();
        }
    }
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String permissions[], @NonNull int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSION_RECORD_AUDIO_REQUEST_CODE: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mp = MediaPlayer.create(this, R.raw.onepiece2);
                    mp.setLooping(true);
                    mp.start();
                    // The permission was granted! Start up the visualizer!
                    // mAudioInputReader = new AudioInputReader(mVisualizerView, this);

                } else {
                    Toast.makeText(this, "Permission for audio not granted. Visualizer can't run.", Toast.LENGTH_LONG).show();
                    finish();
                    // The permission was denied, so we can show a message why we can't run the app
                    // and then close the app.
                }
            }
            // Other permissions could go down here

        }
    }

    protected void onDestroy() {
        super.onDestroy();
        if (mp != null) {
            mp.stop();
            mp.release();
        }
    }
    protected void onPause() {
        super.onPause();
    }





    @Override
    public void onPointerCaptureChanged(boolean hasCapture) {

    }
}

