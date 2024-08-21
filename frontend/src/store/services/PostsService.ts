import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BACKEND_HOST} from "../../constants.ts";
import {TPostItem} from '../../models/PostsModels.ts';

export interface IPostRequest {
  id: number,
  status: string,
  channels: [{
    avatar: string,
    name: string
  }],
  publish_time: string,
  owner_name: string,
  photos: {
    base64: string
  }[],
  html_text: string,
  plain_text: string,
  views: number,
  reactions: number,
  shared: number,
  is_owner: true,
}

export const postsAPI = createApi({
  reducerPath: 'postsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${BACKEND_HOST}`, prepareHeaders: (headers) => {
      headers.set('token', localStorage.getItem('accessToken') as string)
    }
  }),
  tagTypes: ['Posts'],
  endpoints: (build) => ({
    fetchAllPosts: build.query<IPostRequest[], any>({
        query: () => ({url: `/posts`}),
        providesTags: ['Posts']
      }
    ),
    getPostInfo: build.query<TPostItem, any>({
      query: ({id}) => ({url: `/post/${id}`}),
      providesTags: ['Posts']
    }),
    createPost: build.mutation({
        query: (data) => ({
          url: '/posts',
          method: 'POST',
          body: data
        }),
        invalidatesTags: ['Posts']
      }
    ),
    acceptPost: build.mutation({
        query: (data) => ({
          url: `/posts/${data}/accept`,
          method: 'POST',
        }),
        invalidatesTags: ['Posts']
      }
    ),
    rejectPost: build.mutation({
        query: (data) => ({
          url: `/posts/${data}/reject`,
          method: 'DELETE',
          body: data
        }),
        invalidatesTags: ['Posts']
      }
    )
  })
})
