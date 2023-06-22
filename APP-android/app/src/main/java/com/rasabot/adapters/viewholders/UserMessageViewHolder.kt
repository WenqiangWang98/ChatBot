package com.rasabot.adapters.viewholders

import android.view.View
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.rasabot.R

class UserMessageViewHolder(
    itemView:View
): RecyclerView.ViewHolder(itemView) {

    val userMessageTV:TextView = itemView.findViewById(R.id.user_message_tv)

}