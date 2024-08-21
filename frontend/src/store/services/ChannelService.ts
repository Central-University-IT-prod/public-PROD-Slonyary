import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BACKEND_HOST} from "../../constants.ts";

export const channelsAPI = createApi({
  reducerPath: 'usersApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${BACKEND_HOST}`, prepareHeaders: (headers) => {
      headers.set('token', localStorage.getItem('accessToken') as string)
    }
  }),
  tagTypes: ['Channel'],
  endpoints: (build) => ({
    getChannels: build.query({
        query: () => ({url: `/channels/tg`}),
        providesTags: ['Channel']
      }
    ),
    getChannelById: build.query({
      query: (id) => ({url: `/channels/tg/${id}`}),
      providesTags: ['Channel']
    }),
    deleteChannel: build.mutation({
        query: (data) => ({
          url: `/channels/tg/${data}`,
          method: 'DELETE',
        }),
        invalidatesTags: ['Channel']
      }
    )
  })
})